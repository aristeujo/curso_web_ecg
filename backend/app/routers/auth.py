from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.db_models import User
from backend.app.models.user import UserCreate, UserOut, UserLogin, TokenWithUser
from backend.app.utils.security import hash_password
from backend.app.services.auth_user import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
   name_norm = payload.name.strip()
   email_norm = payload.email
   phone_norm = payload.phone

   exists = (
      db.query(User)
      .filter(or_(
         func.lower(User.name) == func.lower(name_norm),    
         func.lower(User.email) == func.lower(email_norm), 
         User.phone == phone_norm,
         )
      ).first()
   )

   if exists:
      raise HTTPException(
         status_code=409,
         detail="name/email/phone já cadastrado"
      )
   
   user = User(
      name=name_norm,
      email=email_norm,
      phone=phone_norm,
      password_hash=hash_password(payload.password)
   )

   db.add(user)
   db.commit()
   db.refresh(user)

   return user

@router.post("/login", response_model=UserOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
   try:
      user = authenticate_user(db, payload)
      
      return user

   except ValueError as e:
      raise HTTPException(
         status_code=401,
         detail=str(e),
      )
