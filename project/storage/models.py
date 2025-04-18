from sqlalchemy import Table, Column, Integer, String, DateTime, ARRAY
from database import metadata
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("status", String, index=True),
    Column("collected_time", DateTime, default=datetime.datetime.utcnow),
    Column("submited_time", DateTime, default=datetime.datetime.utcnow),
    Column("solarPlant", String, index=True),
    Column("video", String, index=True), # function in main.py will generate path for collect files
    Column("image", String, index=True), # function in main.py will generate path for collect files
    Column("weather", String, index=True),
    Column("zone", ARRAY(String), index=True),
    Column("owner", String, index=True),
)

class SolarPlant(Base):
    __tablename__ = 'user_solarplant'

    solarPlant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    solarPlant_name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)