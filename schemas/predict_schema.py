from pydantic import BaseModel, Field
from typing import Literal

class PredictSchema(BaseModel):
    Age: int = Field(..., example=50)
    Sex: Literal["male", "female"] = Field(..., example="male")
    ChestPainType: Literal["ATA", "NAP", "TA"] = Field(..., example="ATA")
    RestingBP: int = Field(..., example=130)
    Cholesterol: int = Field(..., example=220)
    FastingBS: int = Field(..., example=1)  # 0 or 1
    RestingECG: Literal["Normal", "ST", "LVH"] = Field(..., example="ST")
    MaxHR: int = Field(..., example=140)
    ExerciseAngina: Literal["N", "Y"] = Field(..., example="N")
    Oldpeak: float = Field(..., example=2.0)
    ST_Slope: Literal["Up", "Flat", "Down"] = Field(..., example="Flat")
