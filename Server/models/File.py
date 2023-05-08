from pydantic import BaseModel
from pathlib import Path


class File(BaseModel):
    path_file: Path
    date: int
