from fastapi import FastAPI
from config import SUPABASE_KEY, SUPABASE_URL
from supabase import create_client, Client
from request_models import SignupRequest, LoginRequest, LogoutRequest
from fastapi import Body


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()





@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/auth/signup")
async def signup(req: SignupRequest = Body(...)):
    print(req)
    response = supabase.auth.sign_up(
    {"email": req.email, "password": req.password}
)
    print(response)
    supabase.table('users').insert({"id": response.user.id, "first_name": req.first_name, "last_name": req.last_name, "username": req.username, "phone": req.phone, "role": req.role}).execute()
    return response

@app.post("/auth/login")
async def login(req: LoginRequest = Body(...)):
    print(req)
    response = supabase.auth.sign_in_with_password(
    {"email": req.email, "password": req.password}
)
    return {"status": "success", "access_token": response.session.access_token, "refresh_token": response.session.refresh_token}


