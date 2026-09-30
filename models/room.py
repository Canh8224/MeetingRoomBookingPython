from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text
from sqlalchemy.orm import relationship

from database import Base


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    room_name = Column(
        String(100),
        nullable=False
    )

    location = Column(
        String(255),
        nullable=False
    )

    capacity = Column(
        Integer,
        nullable=False
    )

    available = Column(
        Boolean,
        nullable=False
    )

    note = Column(
        Text
    )

    room_equipments = relationship(
        "RoomEquipment",
        back_populates="room",
        cascade="all, delete-orphan"
    )

    images = relationship(
        "RoomImage",
        back_populates="room",
        cascade="all, delete-orphan"
    )

    bookings = relationship(
        "RoomBooking",
        back_populates="room"
    )