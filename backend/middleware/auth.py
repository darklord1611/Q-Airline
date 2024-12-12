from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
from jose.exceptions import JWTError
from config import SUPABASE_JWT_SECRET


# Define routes to exclude from authentication
EXCLUDED_PATHS = ["/", "/docs", "/open-endpoint", "/openapi.json"]

def validate_access_token(token: str):
    """
    Validate the Supabase access token (JWT).
    """
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return payload  # Contains user information
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce authentication on every request except excluded paths.
    """
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for excluded paths
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)
        
        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Authorization header missing or invalid"},
                status_code=401
            )

        # Validate token
        token = auth_header.split("Bearer ")[1]
        try:
            user = validate_access_token(token)
            # Optionally attach user info to the request for further use
            request.state.user = user
        except HTTPException as e:
            return JSONResponse({"detail": e.detail}, status_code=e.status_code)

        # Proceed to the next request handler
        return await call_next(request)
