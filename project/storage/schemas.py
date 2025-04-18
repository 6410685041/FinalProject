from pydantic import BaseModel

class SolarPlantCreate(BaseModel):
    solarPlant_name: str
    location: str