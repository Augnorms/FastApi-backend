from fastapi import FastAPI
from db_connect import engine, Base
from models.user import User
from users_routes import create_user, get_all_users
from logistic_regression_route import linear

#initialise fast api instance
app = FastAPI()

# Create tables automatically (not recommended for production)
# Base.metadata.create_all(bind=engine)

app.include_router(create_user.router, tags=['create-user'])
app.include_router(get_all_users.router, tags=["get-users"])
app.include_router(linear.router, tags=['predict'])
