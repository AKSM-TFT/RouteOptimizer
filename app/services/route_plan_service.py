import uuid
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order
from app.models.route_plan import RoutePlan
from app.api.schemas.route_plan import StopItem, RoutePlanStatus
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
import httpx
import json

OSRM_BASE_URL = "http://router.project-osrm.org"  # swap for self-hosted OSRM later

async def _resolve_and_validate_orders(db: AsyncSession, order_ids: list[str]) -> list[Order]:
    result = await db.execute(
        select(Order).where(Order.id.in_(order_ids)) 
    )
    found = {order.id: order for order in result.scalars().all()} 

    errors = []
    for oid in order_ids:
        order = found.get(oid)
        if order is None:
            errors.append({"order_id": oid, "reason": "not_found"}) 
        elif getattr(order, "active_route_plan_id", None) is not None:  
            errors.append({"order_id": oid, "reason": "already_assigned"})

    if errors:
        raise HTTPException(status_code=400, detail={"invalid_orders": errors}) 

    return [found[oid] for oid in order_ids] 

async def _build_distance_matrix(orders: list[Order]) -> list[list[float]]:
    """
    Calls OSRM's /table endpoint to get real driving distances between all orders.
    Returns an N x N matrix in meters, indexed the same order as `orders`.
    """
    coords = ";".join(f"{o.lng},{o.lat}" for o in orders)  # OSRM wants lng,lat
    url = f"{OSRM_BASE_URL}/table/v1/driving/{coords}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"annotations": "distance"})
        response.raise_for_status()
        data = response.json()

    return data["distances"]


def _solve_tsp(distance_matrix: list[list[float]]) -> list[int]:
    n = len(distance_matrix)
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)  # n stops, 1 vehicle, depot=index 0
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_params)
    if solution is None:
        raise RuntimeError("OR-Tools failed to find a route")

    index = routing.Start(0)
    order = []
    while not routing.IsEnd(index):
        order.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))
    return order

def _build_stop_sequence(orders: list[Order], solved_order: list[int]) -> list[StopItem]:
    return [
        StopItem(
            order_id=orders[solved_order_idx].id,  
            sequence=index,  
            lat=orders[solved_order_idx].lat,
            lng=orders[solved_order_idx].lng,
        )
        for index, solved_order_idx in enumerate(solved_order)  
    ]

async def create_route_plan(db: AsyncSession, driver_id: str, order_ids: list[str]) -> RoutePlan:
    orders = await _resolve_and_validate_orders(db, order_ids)
    distance_matrix = _build_distance_matrix(orders)
    solved_order = _solve_tsp(distance_matrix)
    stop_sequence = _build_stop_sequence(orders, solved_order)

    now = datetime.now(timezone.utc) 

    route_plan = RoutePlan(
        id=str(uuid.uuid4()),          
        driver_id=driver_id,   
        status=RoutePlanStatus.pending,      
        stop_sequence=[order.model_dump() for order in stop_sequence], 
        created_at=now,
        last_updated=now,
    )

    db.add(route_plan)
    await db.commit() 
    await db.refresh(route_plan)
    return route_plan