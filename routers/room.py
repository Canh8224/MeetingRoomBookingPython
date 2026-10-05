from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.room import RoomCreate, RoomResponse
from services.room_service import (
    get_all_rooms,
    get_room_by_id,
    create_room,
    delete_room
)

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.get("/", response_model=list[RoomResponse])
def read_rooms(db: Session = Depends(get_db)):
    return get_all_rooms(db)


@router.get("/{room_id}", response_model=RoomResponse)
def read_room(room_id: int, db: Session = Depends(get_db)):
    room = get_room_by_id(db, room_id)

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy phòng"
        )

    return room


@router.post("/", response_model=RoomResponse)
def add_room(room: RoomCreate, db: Session = Depends(get_db)):
    return create_room(db, room)


@router.delete("/{room_id}")
def remove_room(room_id: int, db: Session = Depends(get_db)):
    result = delete_room(db, room_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy phòng"
        )

    return {
        "message": "Xóa phòng thành công"
    }