from fastapi import APIRouter

from .airports import router as airports_router
from .flights import router as flights_router
from .auth import router as auth_router


router = APIRouter(prefix="/api/v1")

router.include_router(airports_router)
router.include_router(flights_router)
router.include_router(auth_router)

