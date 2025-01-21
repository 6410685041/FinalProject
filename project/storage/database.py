from sqlalchemy import create_engine, MetaData
from databases import Database

from dotenv import load_dotenv
load_dotenv()
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
database = Database(DATABASE_URL)
