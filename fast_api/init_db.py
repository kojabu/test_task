from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base  
from database import engine


# Создание таблиц
Base.metadata.create_all(bind=engine)