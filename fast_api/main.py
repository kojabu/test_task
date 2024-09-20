from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine, SessionLocal
import models
import auth
import crud
from fastapi.templating import Jinja2Templates
from auth import oauth2_bearer, authenticate_user, create_access_token



app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='templates')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Read User by ID
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK )
def read_user(request: Request,user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("detail.html", {
        "request": request,
        "user": db_user  # Pass the user object to the template
    })

# Read all Users
@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# @app.get("/users", status_code=status.HTTP_200_OK)
# def read_all_users(db: db_dependency):
#     users = crud.get_all_users(db)
#     return [{"id": user.id, "email": user.email, "name": user.name, "surname": user.surname, "phone_number": user.phone_number} for user in users]


# # Update User by ID
@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse("edit.html", {
        "request": request,
        "user": db_user
    })

@app.put("/update/{user_id}")


@app.post("/update/{user_id}")
async def update_user(
    user_id: int,
    email: str = Form(...),
    phone_number: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
    db: Session = Depends(get_db)
):
    # Construct user_update dictionary from form data
    user_update = {
        "email": email,
        "phone_number": phone_number,
        "name": name,
        "surname": surname
    }

    # Update user in the database using crud
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return RedirectResponse(url=app.url_path_for('home'), status_code=status.HTTP_303_SEE_OTHER)



# @app.put("/update/{user_id}")
# async def update_user(user_id: int, user_update: dict, db: Session = Depends(get_db)):
#     db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return RedirectResponse(url=app.url_path_for('home',status_code=status.HTTP_303_SEE_OTHER))



# Delete User by ID
@app.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted successfully", "user": db_user}

@app.post("/delete/html/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return RedirectResponse(url=app.url_path_for('home'), status_code=status.HTTP_303_SEE_OTHER)

