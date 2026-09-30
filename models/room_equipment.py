from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class RoomEquipment(Base):
    __tablename__ = "room_equipment"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    room_id = Column(
        "room_id",
        BigInteger,
        ForeignKey(
            "rooms.room_id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    equipment_name = Column(
        "equipment_name",
        String(50),
        ForeignKey(
            "equipments.equipment_name",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    room = relationship(
        "Room",
        back_populates="room_equipments"
    )

    equipment = relationship(
        "Equipment",
        back_populates="room_equipments"
    )