from pydantic import BaseModel
from typing import Optional

class SignupRequest(BaseModel):
    password: str
    email: str
    first_name: str
    last_name: str
    username: Optional[str] = None
    phone : Optional[str] = None
    role: str = "user"


class LoginRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

class LogoutRequest(BaseModel):
    token: str