from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.db_models import User
