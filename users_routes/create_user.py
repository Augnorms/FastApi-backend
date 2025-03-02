from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import get_db
from models.user import User
from schemas.user_schema import UserCreate

router = APIRouter()

@router.post("/createuser")
def create_user(user: UserCreate, db:Session = Depends(get_db)):

    user_already_exist = db.query(User).filter(
        User.first_name == user.first_name,
        User.last_name == user.last_name
    ).first()
    
    if user_already_exist:
        raise HTTPException(status_code=400, detail="Sorry User Already Exist")

    try:
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            gender=user.gender,
            role=user.role
        )

        db.add(new_user)
        db.commit()  #is used to permanently save the changes made in the current transaction to the database
        db.refresh(new_user) # is used to update the SQLAlchemy model instance with the latest data from the database.

        return {
            "data":{
                "code": 200,
                "message": "Success!! User created",
                "data": new_user
            }
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={f'Error {e}'})
