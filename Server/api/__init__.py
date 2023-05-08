from fastapi import APIRouter
from .points import router as point_router
from .files import router as file_router

router = APIRouter(prefix="/v1")
router.include_router(point_router)
router.include_router(file_router)
