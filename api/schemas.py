from pydantic import BaseModel
from datetime import date, time, timedelta
from typing import Optional

class DroneFlightBase(BaseModel):
    drone_type: str
    departure_date: Optional[date]
    departure_time: Optional[time]
    departure_coords: Optional[str]
    arrival_date: Optional[date]
    arrival_time: Optional[time]
    arrival_coords: Optional[str]
    duration: Optional[timedelta]

class DroneFlightCreate(DroneFlightBase):
    flight_id: int

class DroneFlight(DroneFlightBase):
    flight_id: int
    class Config:
        orm_mode = True
