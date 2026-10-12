from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator


class BookingBase(BaseModel):
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None


class BookingCreate(BookingBase):
    @model_validator(mode="after")
    def validate_booking_time(self):
        if self.end_time <= self.start_time:
            raise ValueError("Thời gian kết thúc phải sau thời gian bắt đầu")
        return self


class BookingResponse(BookingBase):
    booking_id: int
    status: str

    class Config:
        from_attributes = True
