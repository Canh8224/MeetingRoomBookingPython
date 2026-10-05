from pydantic import BaseModel
from typing import Optional


class RoomBase(BaseModel):
    room_name: str
    location: str
    capacity: int
    available: bool = True
    note: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomResponse(RoomBase):
    room_id: int

    class Config:
        from_attributes = True