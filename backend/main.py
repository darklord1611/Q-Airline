from fastapi import FastAPI
from config import SUPABASE_KEY, SUPABASE_URL
from supabase import create_client, Client
from fastapi import Body
from api.index import router as api_router

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    api_router, tags=["api"]
)

