

from fastapi import APIRouter, Body
from supabase_client import supabase
from utils.request_models import SignupRequest, LoginRequest

router = APIRouter(prefix="/auth")

@router.post("/signup")
async def signup(req: SignupRequest = Body(...)):
    print(req)
    response = supabase.auth.sign_up(
    {"email": req.email, "password": req.password}
)
    print(response)
    supabase.table('users').insert({"id": response.user.id, "first_name": req.first_name, "last_name": req.last_name, "username": req.username, "phone": req.phone, "role": req.role}).execute()
    return response

@router.post("/login")
async def login(req: LoginRequest = Body(...)):
    print(req)
    response = supabase.auth.sign_in_with_password(
    {"email": req.email, "password": req.password}
)
    return {"status": "success", "access_token": response.session.access_token, "refresh_token": response.session.refresh_token}

