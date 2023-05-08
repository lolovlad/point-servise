from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends

from typing import List

from ..models.Responses import Message
from ..models.Points import PointPost, PointGet

from ..services.PointServices import PointsServices

router = APIRouter(prefix="/points")


@router.post("/{zone}/{type_point}/add_point", responses={
    status.HTTP_201_CREATED: {"model": Message},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message}
})
async def add_point(zone: int, type_point: int, point: PointPost, services: PointsServices = Depends()):
    try:
        await services.add_point(zone, type_point, point)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"message": "point add"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "error add point"})


@router.get("/{zone}/{type_point}/{date}/all_series", response_model=List[PointGet], responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message}
})
async def get_all_series(zone: int, type_point: int, date: str, services: PointsServices = Depends()):
    try:
        response = await services.get_all_series(zone, type_point, date)
        return response
    except FileNotFoundError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "file not found"})


@router.get("/{zone}/{type_point}/{date}/series", response_model=List[PointGet], responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message}
})
async def get_series(zone: int, type_point: int, date: str, start_series: int = 0, end_series: int = 0, services: PointsServices = Depends()):
    try:
        response = await services.get_series(zone, type_point, date, start_series, end_series)
        return response
    except FileNotFoundError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "file not found"})
    except IndentationError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "start <= end"})


@router.get("/{zone}/{type_point}/file/date/series", response_model=List[PointGet], responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message}
})
async def get_date_series(zone: int, type_point: int, start_series: int = 0, end_series: int = 0, services: PointsServices = Depends()):
    try:
        response = await services.get_date_series(zone, type_point, start_series, end_series)
        return response
    except FileNotFoundError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "file not found"})
    except IndentationError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "start <= end"})