from fastapi import FastAPI
from app.core import settings
from app.api.routes import orders

app = FastAPI(
    title="Delivery Route Optimizer",
    version="v1",
    docs_url="/docs" if settings.app_env == "development" else None,  
)

app.include_router(orders.router)

@app.get("/health") 
async def health_check():
    return {"status": "ok"}