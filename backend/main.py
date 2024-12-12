from fastapi import FastAPI
from config import SUPABASE_KEY, SUPABASE_URL
from supabase import create_client, Client
from fastapi import Body
from api.index import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from config import FRONTEND_URL
from middleware.auth import AuthMiddleware
app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(AuthMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    api_router
)

