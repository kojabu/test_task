from sqlalchemy import Column, Integer, String
from dependencies import Base
from sqlalchemy.ext.declarative import declarative_base

# Create the base class for declarative models
Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    hashed_password = Column(String)