from sqlalchemy.orm import Session

from models.room import Room
from schemas.room import RoomCreate


def get_all_rooms(db: Session):
    return db.query(Room).all()


def get_room_by_id(db: Session, room_id: int):
    return db.query(Room).filter(Room.room_id == room_id).first()


def create_room(db: Session, room: RoomCreate):
    new_room = Room(
        room_name=room.room_name,
        location=room.location,
        capacity=room.capacity,
        available=room.available,
        note=room.note
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room


def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.room_id == room_id).first()

    if room is None:
        return False

    db.delete(room)
    db.commit()

    return True