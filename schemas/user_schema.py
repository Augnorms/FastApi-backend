from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    middle_name: Optional[str] = None  # Optional field
    gender: str
    role: str

    model_config = ConfigDict(from_attributes=True)