from typing_extensions import Annotated
from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from pydantic.config import ConfigDict
from pydantic.functional_validators import BeforeValidator

from backend.app.utils.validators import normalize_phone_br

EmailLower = Annotated[EmailStr, BeforeValidator(lambda v: str(v).lower())]
PhoneBR = Annotated[str, BeforeValidator(normalize_phone_br)]

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailLower
    phone: PhoneBR

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)

class UserLogin(BaseModel):
    email: EmailLower
    password: str = Field(..., min_length=6, max_length=72)

class UserOut(UserBase):
    id: int
    name: str
    email: EmailLower
    phone: PhoneBR
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenWithUser(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

