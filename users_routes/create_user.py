from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from db_connect import get_db
from models.user import User
from schemas.user_schema import UserCreate

router = APIRouter()

def send_welcome_email(first_name: str, last_name: str):
    # Simulate email sending
    print(f"Sending welcome email to {first_name} {last_name}...")

@router.post("/createuser")
def create_user(
    user: UserCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user_already_exist = db.query(User).filter(
        User.first_name == user.first_name,
        User.last_name == user.last_name
    ).first()
    
    if user_already_exist:
        raise HTTPException(status_code=400, detail="Sorry, User Already Exists")

    try:
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            gender=user.gender,
            role=user.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # ✅ Add the email sending task to background
        background_tasks.add_task(send_welcome_email, user.first_name, user.last_name)

        return {
            "data": {
                "code": 200,
                "message": "Success!! User created",
                "data": new_user
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error {e}')
