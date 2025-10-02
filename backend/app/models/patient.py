from datetime import date
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from pydantic.config import ConfigDict

from backend.app.utils.validators import parse_birth_date, normalize_phone_br

EmailLower = Annotated[EmailStr, BeforeValidator(lambda v: str(v).lower())]
PhoneBR = Annotated[str, BeforeValidator(normalize_phone_br)]
BirthDateParsed = Annotated[Optional[date], BeforeValidator(parse_birth_date)]

class PatientBase(BaseModel):
    name: str = Field(..., min_length = 5, max_length = 60, description = "Nome do paciente",)
    birth_date: BirthDateParsed = None
    email: EmailLower
    phone: PhoneBR

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = Field(..., min_length = 5, max_length = 60, description = "Nome do paciente",)
    birth_date: Optional[BirthDateParsed] = None
    email: Optional[EmailLower]
    phone: Optional[PhoneBR]

class PatientOut(PatientBase):
    model_config = ConfigDict(from_atributes=True)
    id: int