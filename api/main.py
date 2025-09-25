import os
import shutil
import pandas as pd
import uuid
from fastapi import FastAPI, UploadFile, File, Depends
from database import SessionLocal, Base, engine
import crud, schemas
import aiofiles

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-flights/", status_code=202)
async def upload_flights(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    dest = f"/data/uploads/{file_id}.xlsx"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    async with aiofiles.open(dest, "wb") as f:
        while chunk := await file.read(1024*1024):
            await f.write(chunk)
    from celery_app import parse_and_store
    parse_and_store.delay(dest, file_id)
    return {"task_id": file_id}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    return {"status": "PENDING", "detail": {}}

@app.get("/flights/", response_model=list[schemas.DroneFlight])
def list_flights(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud.get_drone_flights(db, skip, limit)

def run_parser(path: str) -> pd.DataFrame:
    out = path.replace(".xlsx", ".csv")
    os.system(f"python drone_parser.py {path} -o {out}")
    return pd.read_csv(out)

def get_db_session():
    return SessionLocal()
