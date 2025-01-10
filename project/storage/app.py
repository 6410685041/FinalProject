from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI()

# สร้างโมเดลสำหรับ task
class Task(BaseModel):
    name: str
    date_time: datetime

# API สำหรับรับข้อมูล task พร้อมไฟล์
@app.post("/upload-task/")
async def upload_task(file: UploadFile = File(...), name: str = Form(...), date_time: datetime = Form(...)):
    # task = Task(name=name, date_time=date_time)
    # # บันทึกไฟล์ อาจจะบันทึกลงในระบบไฟล์หรือฐานข้อมูล
    # contents = await file.read()
    # with open(f"{file.filename}", "wb") as f:
    #     f.write(contents)
    # # บันทึก task ลงในฐานข้อมูล (ตัวอย่างไม่ได้เชื่อมต่อจริง)
    # # save_task_to_db(task)
    # return {"filename": file.filename, "task": task}
    return None

# API สำหรับรับข้อมูล JSON และบันทึกลงฐานข้อมูล
@app.post("/tasks/")
async def create_task(task: Task):
    # save_task_to_db(task) (ตัวอย่างไม่ได้เชื่อมต่อจริง)
    # return {"task": task}
    return None

# สามารถเพิ่ม API เพื่อส่งข้อมูล task ที่มีอยู่แล้วในฐานข้อมูล หากจำเป็น
@app.get("/tasks/")
async def get_tasks():
    # tasks = fetch_tasks_from_db() (ตัวอย่างไม่ได้เชื่อมต่อจริง)
    # return {"tasks": tasks}
    # return {"tasks": "Placeholder for tasks from database"}
    return None

