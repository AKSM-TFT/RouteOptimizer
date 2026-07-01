from fastapi import Header, HTTPException

async def get_current_driver_id(x_driver_id: str = Header(...)) -> str:
    """
    TEMPORARY STUB — no real auth yet.
    Reads driver identity from a header instead of a verified JWT.
    Replace with JWT decode + signature verification before any
    non-local deployment. Anyone can spoof X-Driver-Id right now.
    """
    if not x_driver_id:
        raise HTTPException(status_code=401, detail="Missing driver identity")
    return x_driver_id