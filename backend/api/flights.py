

from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/flights")
async def get_flights():
    return {"flights": "flights"}
