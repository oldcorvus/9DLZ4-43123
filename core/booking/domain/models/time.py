from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, timedelta

class ReservationTime(BaseModel):
    start_time: datetime
    end_time: datetime
    duration: timedelta = None

    @field_validator("end_time")
    @classmethod
    def validate_timing(cls, v, values):
        if "start_time" in values.data and v <= values.data["start_time"]:
            raise ValueError("End time must be after start time")
        return v

    @property
    def duration(self) -> timedelta:
        return self.end - self.start