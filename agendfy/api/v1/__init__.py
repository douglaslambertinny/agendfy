from fastapi import APIRouter

from . import (
    hello_world,
    company,
    user,
    appointment,
)

router = APIRouter(
    prefix="/v1",
)

router.include_router(hello_world.router)
router.include_router(appointment.router)
router.include_router(company.router)
router.include_router(user.router)