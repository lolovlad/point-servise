from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi import status
from ..models.Responses import Message
from ..services.FileServices import FileServices
from ..services.PointServices import PointsServices
import asyncio

router = APIRouter(prefix="/files")


async def delete_file(service, path_file):
    await asyncio.sleep(3)
    service.delete_file(path_file)


@router.get("/{zone}/{type_point}/download/{date}", responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message}
})
async def download_file(zone: int, type_point: int, date: str, type_series: str, back_task: BackgroundTasks, start: int | None = 0, end: int | None = 0, services: FileServices = Depends(),
                        points_services: PointsServices = Depends()):
    try:
        if type_series == "allFile":
            path_file = services.get_file(zone, type_point, date)
        elif type_series == "timeSeries":
            points = await points_services.get_series(zone, type_point, date, start, end)
            path_file = services.get_new_file(points)
        elif type_series == "dateSeries":
            points = await points_services.get_date_series(zone, type_point, start, end)
            path_file = services.get_new_file(points)
        response = FileResponse(
            path=path_file,
            filename=f"температура за {date}.csv",
            media_type='multipart/form-data',
        )
        if type_series != "allFile":
            back_task.add_task(delete_file, services, path_file)
        return response
    except FileNotFoundError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "file not found"})
