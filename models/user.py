from sqlalchemy import Column, Integer, String
from db_connect import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    gender = Column(String(10), nullable=False)
    role = Column(String(20), nullable=False)


