from ..repositories.FileRepository import FileRepository
from random import randint
from fastapi import Depends
from ..models.Points import PointGet
from typing import List
import os


class FileServices:
    def __init__(self, repo: FileRepository = Depends()):
        self.__repo: FileRepository = repo

    def get_file(self, zone: int, type_data: int, file_name: str) -> str:
        file_name = f"{zone}/{file_name}T{type_data}.csv"
        self.__repo.set_file(file_name)
        if self.__repo.is_file_exist():
            return self.__repo.get_file_name()
        else:
            raise FileNotFoundError

    def get_new_file(self, points: List[PointGet]) -> str:
        random_name = f"{randint(10000, 1000000)}.csv"
        self.__repo.set_file(random_name)
        self.__repo.create_file(list(points[0].dict().keys()))
        self.__repo.add_list(points)
        path_file = self.__repo.get_file_name()
        return self.__repo.get_file_name()

    def delete_file(self, path_file):
        os.remove(path_file)