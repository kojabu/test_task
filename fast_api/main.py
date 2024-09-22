from fastapi import FastAPI
from dependencies import engine, SessionLocal
from models.user import Base
import routers.auth as auth
import routers.user as user


app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", status_code=200)
def root():
    return {"message": "Welcome to the User Management API"}

