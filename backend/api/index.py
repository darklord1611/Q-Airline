from fastapi import APIRouter

from .airports import router as airports_router
from .flights import router as flights_router
from .auth import router as auth_router
from .bookings import router as bookings_router
from .notifications import router as notifications_router
from .news import router as news_router
from .services import router as services_router
from .aircrafts import router as aircrafts_router
from .discounts import router as discounts_router

router = APIRouter(prefix="/api/v1")

router.include_router(airports_router)
router.include_router(flights_router)
router.include_router(auth_router)
router.include_router(bookings_router)
router.include_router(notifications_router)
router.include_router(news_router)
router.include_router(services_router)
router.include_router(aircrafts_router)
router.include_router(discounts_router)
