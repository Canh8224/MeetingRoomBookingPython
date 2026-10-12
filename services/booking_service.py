from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.room import Room
from models.room_booking import RoomBooking
from schemas.booking import BookingCreate


def get_all_bookings(db: Session):
    return db.query(RoomBooking).all()


def get_booking_by_id(db: Session, booking_id: int):
    return db.query(RoomBooking).filter(
        RoomBooking.booking_id == booking_id
    ).first()


def create_booking(db: Session, booking: BookingCreate):
    room = db.query(Room).filter(
        Room.room_id == booking.room_id
    ).first()

    if room is None:
        raise ValueError("Không tìm thấy phòng họp")

    if not room.available:
        raise ValueError("Phòng họp hiện không khả dụng")

    user_exists = db.query(RoomBooking.user_id).filter(
        RoomBooking.user_id == booking.user_id
    ).first()

    from models.user import User

    user = db.query(User).filter(
        User.user_id == booking.user_id
    ).first()

    if user is None:
        raise ValueError("Không tìm thấy người dùng")

    conflict = db.query(RoomBooking).filter(
        and_(
            RoomBooking.room_id == booking.room_id,
            RoomBooking.status != "CANCELLED",
            RoomBooking.start_time < booking.end_time,
            RoomBooking.end_time > booking.start_time
        )
    ).first()

    if conflict:
        raise ValueError("Phòng đã có lịch đặt trong khoảng thời gian này")

    new_booking = RoomBooking(
        room_id=booking.room_id,
        user_id=booking.user_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        status="PENDING",
        purpose=booking.purpose
    )

    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
    except Exception:
        db.rollback()
        raise


def cancel_booking(db: Session, booking_id: int):
    booking = get_booking_by_id(db, booking_id)

    if booking is None:
        return None

    booking.status = "CANCELLED"
    db.commit()
    db.refresh(booking)

    return booking
