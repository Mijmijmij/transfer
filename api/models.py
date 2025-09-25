from sqlalchemy import Column, Integer, Text, Date, Time, Interval
from database import Base

class DroneFlight(Base):
    __tablename__ = "drone_flights"
    flight_id = Column(Integer, primary_key=True, index=True)
    drone_type = Column(Text, nullable=False)
    departure_date = Column(Date)
    departure_time = Column(Time)
    departure_coords = Column(Text)
    arrival_date = Column(Date)
    arrival_time = Column(Time)
    arrival_coords = Column(Text)
    duration = Column(Interval)
