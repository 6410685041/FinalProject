from fastapi import FastAPI, File, UploadFile, HTTPException, status,  Depends, Request, Form
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from database import database, SessionLocal
from models import Task, SolarPlant, Owner
from schemas import SolarPlantCreate, TaskUpload

import json
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
import re
import pytz

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


# About Solar Plant
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
def create_solarplant(solar_plant: SolarPlantCreate):
    db = SessionLocal()
    try:
        # check if input is correct
        if len(solar_plant.solarPlant_name) < 5:
            return {"message": "This name is too short."}
        elif not is_valid_coordinate(solar_plant.location):
            return {"message": "Location is incorrect."}

        # Check if the solar plant name already exists
        existing_plant = db.query(SolarPlant).filter(SolarPlant.solarPlant_name == solar_plant.solarPlant_name).first()
        if existing_plant:
            return {"message": "This name is already exists."}
        
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

# function for checking location
def is_valid_coordinate(location):
    pattern = r"^-?\d+(\.\d+)?, ?-?\d+(\.\d+)?$"
    return bool(re.match(pattern, location))


# About Task
@app.post("/Task/upload_task")
async def create_task(
        # task: TaskUpload,
        task_form: str = Form(...),
        video: Optional[UploadFile] = File(None),
        image: Optional[UploadFile] = File(None)
        ):
    db = SessionLocal()
    try:
        task_data = json.loads(task_form)
        task = TaskUpload(**task_data)
        file = {'video':'None', 'image':'None'}
        # check input
        if not (file['video'] or file['image']) :
            return {"message": "Please provide either an image or a video."}
        elif not (task.solarPlant_id and task.weather and task.owner and task.temperature):
            return {"message": "All fields (solarPlant, weather, owner, temperature) must be provided."}
        else: # check time
            current_utc_time = datetime.now(pytz.utc)
            if task.upload_time > current_utc_time:
                return {"message": "Upload time must be in the past"}
            elif task.collected_time > task.upload_time:
                return {"message": "Collected time must be before or at the upload time."}

        # create a Task first
        task_query = Task(
            status=False, # this task is in waiting queue
            collected_time=task.collected_time,
            upload_time=task.upload_time,
            weather=task.weather,
            temperature=task.temperature,
            solarPlant_id=task.solarPlant_id, # Foreign Key
            owner_id=task.owner # Foreign Key
        )

        # task_id = await database.execute(task_query)
        db.add(task_query)
        db.commit()
        db.refresh(task_query)
        task_id = task_query.id

        # Save the files with the task_id in their paths
        video_path = await save_upload_file(file['video'], task_id, "video") if file['video'] else None
        image_path = await save_upload_file(file['image'], task_id, "image") if file['image'] else None

        # Update the task with file paths
        update_query = Task.update().where(Task.c.id == task_id).values(video=video_path, file=image_path)
        await database.execute(update_query)

        return {"task_id": task_id, "video_path": video_path, "image_path": image_path}
    except HTTPException as he:
        db.rollback()
        return {"error": str(he.detail)}, he.status_code
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()

async def save_upload_file(upload_file: UploadFile, task_id: int, file_type: str):
    directory = f"./SolarData/{task_id}"
    os.makedirs(directory, exist_ok=True)
    file_location = f"./SolarData/{task_id}/{file_type}/{upload_file.filename}"
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(upload_file.file, file_object)
    return file_location

@app.get("/Task/total")
def find_all_task():
    db = SessionLocal()
    try:
        query = text("SELECT \"id\", \"owner_id\", \"collected_time\" FROM process_task")
        result = db.execute(query).fetchall()

        result_list = [{
                            'id': str(row[0]), 
                            'owner_name': find_user(db, row[1]), 
                            'upload_time': row[2].strftime("%B %d, %Y, %I:%M %p") if row[2] else None
                        }for row in result]
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()  # Make sure to close the session
    return json.dumps(result_list)

def find_user(db: Session, user_id: int):
    user = db.query(Owner).filter(Owner.id == user_id).first()
    if user:
        return user.username  # หรือ .username แล้วแต่ model
    return None