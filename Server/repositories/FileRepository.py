from pathlib import Path
import os
from ..models.Points import PointPost, PointGet
import csv
from settings import settings
from typing import List


class FileRepository:
    def __init__(self):
        self.__path_file = Path(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent,
                                     settings.static_file)

        self.__path_file_now: Path = None

    def create_dir(self):
        if self.__path_file_now.suffix:
            path_folders = self.__path_file_now.parent
        else:
            path_folders = self.__path_file_now
        while not os.path.exists(path_folders):
            os.makedirs(path_folders)

    def get_path(self):
        return self.__path_file

    def get_file(self):
        return self.__path_file_now

    def set_file(self, file_name: str):
        self.__path_file_now = Path(self.__path_file, file_name)

    def is_file_exist(self):
        return os.path.exists(self.__path_file_now)

    def create_file(self, header: list):
        with open(self.__path_file_now, "w", newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=list(header)
            )
            writer.writeheader()

    def add(self, point: PointPost):
        with open(self.__path_file_now, "a", newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=list(point.dict().keys())
            )
            writer.writerow(point.dict())

    def get_series(self, start: int, end: int) -> List[PointGet]:
        list_point = []
        with open(self.__path_file_now, "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                point = PointGet(**row)
                if start <= point.time_from_second <= end:
                    list_point.append(point)
        return list_point

    def get_all_series(self) -> List[PointGet]:
        with open(self.__path_file_now, "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            list_point = [PointGet(**row) for row in reader]
            list_point.sort(key=lambda x: x.time_from_second)
            return list_point

    def get_file_name(self) -> str:
        return str(self.__path_file_now)

    def delete_file(self):
        os.remove(self.__path_file_now)

    def add_list(self, points: List[PointGet]):
        with open(self.__path_file_now, "a", newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=list(points[0].dict().keys())
            )
            for point in points:
                writer.writerow(point.dict())