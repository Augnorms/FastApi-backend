from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import get_db
from models.user import User
from schemas.user_schema import UserCreate  # Create a schema for response

router = APIRouter()

@router.get("/users", response_model=dict)
def get_users(db: Session = Depends(get_db)):
    try:
        fetch_all_users = db.query(User).all()

        if not fetch_all_users:
            raise HTTPException(status_code=404, detail="No users found")

        # Convert SQLAlchemy objects to dictionaries
        user_list = [UserCreate.model_validate(user).model_dump() for user in fetch_all_users]


        return {
            "status": 200,
            "message": "Success!!",
            "count": len(user_list),
            "data": user_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
