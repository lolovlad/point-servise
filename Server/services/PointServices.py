from ..models.Points import PointPost, PointGet
from ..models.File import File
from ..repositories.FileRepository import FileRepository
from fastapi import Depends
from datetime import date
from pathlib import Path
import bisect
from typing import List
import os


class PointsServices:
    def __init__(self, repo: FileRepository = Depends()):
        self.__repo: FileRepository = repo

    def __paser_file_path(self, file_name: str) -> File:
        self.__repo.set_file(file_name)
        year, mounc, day = map(int, file_name.split(".")[0].split("-"))
        date_to_day = year * 365 + mounc * 31 + day
        file = File(
            path_file=self.__repo.get_path(),
            date=date_to_day
        )
        return file

    async def add_point(self, zone: int, type_point: int, point: PointPost):
        now_file = f"{zone}/{date.today().isoformat()}T{type_point}.csv"
        self.__repo.set_file(now_file)
        self.__repo.create_dir()
        if self.__repo.is_file_exist() is False:
            self.__repo.create_file(list(point.dict().keys()))
        self.__repo.add(point)

    async def get_all_series(self, zone: int, type_point: int, file_name: str) -> List[PointGet]:
        file_name = f"{zone}/{file_name}T{type_point}.csv"
        self.__repo.set_file(file_name)
        if self.__repo.is_file_exist():
            return self.__repo.get_all_series()
        else:
            raise FileNotFoundError

    async def get_series(self, zone: int, type_point: int, file_name: str,
                         start_series: int,
                         end_series: int) -> List[PointGet]:
        if start_series >= end_series:
            raise IndentationError
        file_name = f"{zone}/{file_name}T{type_point}.csv"
        self.__repo.set_file(file_name)
        if self.__repo.is_file_exist():
            return self.__repo.get_series(start_series, end_series)
        else:
            raise FileNotFoundError

    async def get_date_series(self, zone: int, type_point: int, start_series: int, end_series: int) -> List[PointGet]:
        if start_series >= end_series:
            raise IndentationError
        path_file = self.__repo.get_path()
        points = []

        for name_file in os.listdir(Path(path_file, str(zone), str(type_point))):
            file = self.__paser_file_path(name_file)
            if start_series <= file.date <= end_series:
                self.__repo.set_file(name_file)
                points += self.__repo.get_all_series()
        return points
