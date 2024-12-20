

from fastapi import APIRouter, Body
from supabase_client import supabase
from utils.request_models import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(req: RegisterRequest):
    print(req)
    response = supabase.auth.sign_up(
    {"email": req.email, "password": req.password}
)
    user_response = supabase.table('users').insert({"id": response.user.id, "first_name": req.first_name, "last_name": req.last_name, "username": req.username, "phone": req.phone, "role": req.role}).execute().data
    return {"status": "success", "data": user_response}

@router.post("/login")
async def login(req: LoginRequest):
    print(req)
    response = supabase.auth.sign_in_with_password(
    {"email": req.email, "password": req.password}
)
    user = supabase.table('users').select("id", "first_name", "last_name", "role", "phone").eq('id', response.user.id).execute().data[0]
    user["email"] = req.email
    user["access_token"] = response.session.access_token
    user["refresh_token"] = response.session.refresh_token
    return {"status": "success", "data": user}

