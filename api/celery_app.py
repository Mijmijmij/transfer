from celery import Celery
import os

broker = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
celery = Celery("drones", broker=broker, backend=broker)

@celery.task(name="celery_app.parse_and_store")
def parse_and_store(path, file_id):
    from main import run_parser, get_db_session, crud, schemas
    import os
    df = run_parser(path)
    db = get_db_session()
    for rec in df.to_dict(orient="records"):
        flight = schemas.DroneFlightCreate(**rec)
        crud.create_drone_flight(db, flight)
    db.close()
