from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from crud.user import get_all_users, get_user, update_user, delete_user 
from dependencies import get_db  

router = APIRouter()

# Read all Users 
@router.get("/users/all", status_code=status.HTTP_200_OK)
async def get_users_endpoint(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return [
        {
            "id": user.id,
            "email": user.email,
            "phone_number": user.phone_number,
            "name": user.name,
            "surname": user.surname
        } for user in users
    ]



# Read User by ID 
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": db_user.id,
        "email": db_user.email,
        "phone_number": db_user.phone_number,
        "name": db_user.name,
        "surname": db_user.surname
    }


# Update User by ID
@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_endpoint(
    user_id: int,
    email: str = Form(...),
    phone_number: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
    db: Session = Depends(get_db)
):
    user_update = {
        "email": email,
        "phone_number": phone_number,
        "name": name,
        "surname": surname
    }

    # Update user in the database using CRUD
    db_user = update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "status": "User updated successfully",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "phone_number": db_user.phone_number,
            "name": db_user.name,
            "surname": db_user.surname
        }
    }

# Delete User by ID 
@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted successfully", "user": db_user}
