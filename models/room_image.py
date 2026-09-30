from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class RoomImage(Base):
    __tablename__ = "room_images"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    url = Column(
        String(255),
        nullable=False
    )

    room_id = Column(
        "room_id",
        BigInteger,
        ForeignKey("rooms.room_id"),
        nullable=False
    )

    room = relationship(
        "Room",
        back_populates="images"
    )