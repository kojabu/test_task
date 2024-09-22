from sqlalchemy.orm import Session
from models.user import User


# Read all Users 
def get_all_users(db: Session):
    return db.query(User).all()


# Read User by ID 
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# Update User by ID
def update_user(db: Session, user_id: int, user_update: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    
    db_user.email = user_update.get("email", db_user.email)
    db_user.phone_number = user_update.get("phone_number", db_user.phone_number)
    db_user.name = user_update.get("name", db_user.name)
    db_user.surname = user_update.get("surname", db_user.surname)
    
    db.commit()
    db.refresh(db_user)
    return db_user


# Delete User by ID 
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()
    return db_user

















# def get_all_users(db: Session):
#     return db.query(models.User).all()

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

# def update_user(db: Session, user_id: int, user_update: models.User):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user is None:
#         return None
    
#     db_user.email = user_update.get("email")
#     db_user.phone_number = user_update.get("phone_number")
#     db_user.name = user_update.get("name")
#     db_user.surname = user_update.get("surname")
    
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def delete_user(db: Session, user_id: int):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user is None:
#         return None

#     db.delete(db_user)
#     db.commit()
#     return db_user