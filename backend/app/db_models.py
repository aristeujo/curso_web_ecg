# backend/app/db_models.py
from sqlalchemy import String, Date, DateTime, UniqueConstraint, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from backend.app.database import Base


# -----------------------------
# Usuário
# -----------------------------
class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("name", name="uq_users_name"),
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("phone", name="uq_users_phone"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True) 
    birth_date: Mapped[Date | None] = mapped_column(Date, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # triages: Mapped[list["Triage"]] = relationship(
    #     back_populates="patient", 
    #     cascade="all, delete-orphan",
    #     passive_deletes=True,
    # )