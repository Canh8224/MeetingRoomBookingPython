from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


class RoomBooking(Base):
    __tablename__ = "room_bookings"

    booking_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    room_id = Column(
        "roomId",
        BigInteger,
        ForeignKey("rooms.room_id"),
        nullable=False
    )

    user_id = Column(
        "userId",
        BigInteger,
        ForeignKey("users.user_id"),
        nullable=False
    )

    start_time = Column(
        "startTime",
        DateTime,
        nullable=False
    )

    end_time = Column(
        "endTime",
        DateTime,
        nullable=False
    )

    status = Column(
        "status",
        String(50),
        nullable=False
    )

    purpose = Column(
        "purpose",
        Text,
        nullable=True
    )

    room = relationship(
        "Room",
        back_populates="bookings"
    )

    user = relationship(
        "User"
    )