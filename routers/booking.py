from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.booking import BookingCreate, BookingResponse
from services.booking_service import (
    get_all_bookings,
    get_booking_by_id,
    create_booking,
    cancel_booking
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=list[BookingResponse])
def read_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)


@router.get("/{booking_id}", response_model=BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy lịch đặt phòng"
        )

    return booking


@router.post("/", response_model=BookingResponse)
def add_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        return create_booking(db, booking)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/{booking_id}/cancel", response_model=BookingResponse)
def remove_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = cancel_booking(db, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy lịch đặt phòng"
        )

    return booking
