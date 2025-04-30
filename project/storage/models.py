from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Float, ForeignKey, JSON, Table
from database import metadata
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class SolarPlant(Base):
    __tablename__ = 'user_solarplant'

    solarPlant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    solarPlant_name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)

class Owner(Base):
    __tablename__ = 'user_user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)

process_task_zones = Table(
    "process_task_zones",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("process_task.id")),
    Column("zone_id", Integer, ForeignKey("process_zone.id"))
)

class Zone(Base):
    __tablename__ = 'process_zone'

    id = Column(Integer, primary_key=True)
    zone_name = Column(String(256))
    points = Column(JSON, default=list)

    tasks = relationship(
        "Task",
        secondary="process_task_zones",
        back_populates="zones"
    )

class Task(Base):
    __tablename__ = 'process_task'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    temperature = Column(Float)
    weather = Column(String, index=True)
    
    # Foreign Key
    owner_id = Column(Integer, ForeignKey('user_user.id'))
    owner = relationship("Owner")
    solarPlant_id = Column(String, ForeignKey('user_solarplant.solarPlant_id'))
    solarPlant = relationship("SolarPlant")

    # Add in the future
    zones = relationship(
        "Zone",
        secondary="process_task_zones",
        back_populates="tasks"
    )

    # Time
    collected_time = Column(DateTime)
    submitted_time = Column(DateTime, nullable=True) # will Add in the future
    upload_time = Column(DateTime)

    # Files
    video = Column(String, index=True, nullable=True) # function in app.py will generate path for collect files
    file = Column(String, index=True, nullable=True) # function in app.py will generate path for collect files

