from pydantic import BaseModel, Field, validator
from typing import Optional


class PointPost(BaseModel):
    time: str
    data: float


class PointGet(BaseModel):
    time: str
    data: float
    time_from_second: Optional[int] = Field(alias="_time_from_second")

    @validator("time_from_second", always=True)
    def set_time_second(cls, v, values, **kwargs):
        hours, minutes, seconds = map(int, values.get("time").split("."))
        seconds = hours * 60 * 60 + minutes * 60 + seconds
        return v or seconds
