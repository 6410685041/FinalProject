from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status,  Depends
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from database import database, SessionLocal
from models import tasks, SolarPlant
from schemas import SolarPlantCreate

import json
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

origins = [
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins
    allow_credentials=True,  # Allow cookies
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Setup database engine and session
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/SolarPlant/all")
def find_all_solarplant():
    db = SessionLocal()
    try:
        query = text("SELECT \"solarPlant_id\", \"solarPlant_name\" FROM user_solarplant")
        result = db.execute(query).fetchall()
        result_list = [{'solarPlant_id': str(row[0]), 'solarPlant_name': row[1]} for row in result]
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()  # Make sure to close the session
    return json.dumps(result_list)

@app.get("/SolarPlant/data")
def find_all_solarplant():
    db = SessionLocal()
    try:
        query = text("SELECT \"solarPlant_name\", \"location\" FROM user_solarplant")
        result = db.execute(query).fetchall()
        result_list = [{'solarPlant_name': str(row[0]), 'location': row[1]} for row in result]
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()  # Make sure to close the session
    return json.dumps(result_list)

@app.post("/SolarPlant/create")
def create_solarplant(solar_plant: SolarPlantCreate, db: Session = Depends(get_db)):
    db = SessionLocal()
    try:
        # Check if the solar plant name already exists
        existing_plant = db.query(SolarPlant).filter(SolarPlant.solarPlant_name == solar_plant.solarPlant_name).first()
        if existing_plant:
            return {"message": "This name is already exists."}
            # return HTTPException(status_code=400, detail="This name is already exists")
        
        # Create new solar plant if the name does not exist
        new_plant = SolarPlant(solarPlant_name=solar_plant.solarPlant_name, location=solar_plant.location)
        db.add(new_plant)
        db.commit()
        db.refresh(new_plant)
        return {"message": "Solar plant created successfully."}
    except HTTPException as he:
        db.rollback()
        return {"error": str(he.detail)}, he.status_code
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()

@app.post("/tasks/")
async def create_task(
        status: str = Form(None), # Set to default
        solarPlant: str = Form(...),
        weather: str = Form(...),
        zone: List[str] = Form(...),
        owner: str = Form(...),
        video: UploadFile = File(None),  # Optional file
        image: UploadFile = File(None),  # Optional file
        collected_time: datetime = Form(...),
        temperature: float = Form(...),
    ):

    # insert the task without file paths
    task_query = tasks.insert().values(
        status=False, # this task is in waiting queue
        collected_time=collected_time,
        submited_time=datetime.now(),  # fixed datetime usage
        solarPlant=solarPlant,
        weather=weather,
        zone=zone,
        owner=owner,
        temperature=temperature,
    )
    task_id = await database.execute(task_query)

    # Save the files with the task_id in their paths
    video_path = await save_upload_file(video, task_id, "video") if video else None
    image_path = await save_upload_file(image, task_id, "image") if image else None

    # Update the task with file paths
    update_query = tasks.update().where(tasks.c.id == task_id).values(video=video_path, image=image_path)
    await database.execute(update_query)

    return {"task_id": task_id, "video_path": video_path, "image_path": image_path}

async def save_upload_file(upload_file: UploadFile, task_id: int, file_type: str):
    directory = f"./SolarData/{task_id}"
    os.makedirs(directory, exist_ok=True)
    file_location = f"./SolarData/{task_id}/{file_type}/{upload_file.filename}"
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(upload_file.file, file_object)
    return file_location
