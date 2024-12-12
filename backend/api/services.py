

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateAircraftRequest

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", description="Get all services")
async def get_services(
):
    services = supabase.table("services").select().execute().data
    return {"status" : "success", "data": services}


@router.get("/search", description="Get all services that match the search criteria")
async def get_services_by_criteria(service_type: str):
    services = supabase.table("services").select("id", "name", "description", "img_src", "price").eq("type", service_type).execute().data
    for service in services:
        service["quantity"] = 0
    return {"status" : "success", "data": services}

