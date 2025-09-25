from sqlalchemy.orm import Session
from models import DroneFlight
from schemas import DroneFlightCreate

def create_drone_flight(db: Session, flight: DroneFlightCreate):
    db_obj = DroneFlight(**flight.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_drone_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DroneFlight).offset(skip).limit(limit).all()
