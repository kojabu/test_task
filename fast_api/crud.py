from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import models



def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: models.User):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    
    db_user.email = user_update.get("email")
    db_user.phone_number = user_update.get("phone_number")
    db_user.name = user_update.get("name")
    db_user.surname = user_update.get("surname")
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
