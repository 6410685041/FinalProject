from pydantic import BaseModel
from datetime import datetime

class SolarPlantCreate(BaseModel):
    solarPlant_name: str
    location: str

class TaskUpload(BaseModel):
    solarPlant_id: str
    weather: str
    collected_time: datetime
    upload_time: datetime
    temperature: float
    owner: int

    class Config:
        arbitrary_types_allowed = True