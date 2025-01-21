from fastapi import FastAPI, File, UploadFile, Form
from typing import List

from fastapi import FastAPI
from database import database
from models import tasks
from typing import List
from datetime import datetime

import os

app = FastAPI()

@app.post("/tasks/")
async def create_task(
        status: str = Form(...),
        solarPlant: str = Form(...),
        weather: str = Form(...),
        zone: List[str] = Form(...),
        owner: str = Form(...),
        video: UploadFile = File(None),  # Optional file
        image: UploadFile = File(None),  # Optional file
        collected_time: datetime = Form(...),
    ):

    # insert the task without file paths
    task_query = tasks.insert().values(
        status=status, 
        collected_time=collected_time,
        submited_time=datetime.now(),  # fixed datetime usage
        solarPlant=solarPlant,
        weather=weather,
        zone=zone,
        owner=owner
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
