from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db_models import Patient
from backend.app.models.patient import PatientCreate, PatientUpdate

def create_patient(db: Session, payload:PatientCreate) -> Patient:
    data = payload.model_dump(exclude_unset=True)
    obj = Patient(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

def get_patient(db: Session, patient_id: int) -> Patient:
    obj = db.get(Patient, patient_id)
    print(obj)

    if not obj:
        raise ValueError("patient not-found")
    return obj

def list_patients(db: Session, page: int = 1, size: int = 50) -> List[Patient]:
    return (
        db.query(Patient)
        .order_by(Patient.id.asc())
        .offset((page-1)*size)
        .limit(size)
        .all()
    )
    
def search_patients_by_name(db: Session, patient_name: str) -> List[Patient]:
    return(
        db.query(Patient)
        .filter(func.lower(Patient.name).like(f"%{patient_name.lower()}%"))
        .order_by(Patient.name.asc())
        .all()
    )

def update_patient(db: Session, patient_id: int, payload: PatientUpdate) -> Patient:
    obj = get_patient(db, patient_id)
    data = payload.model_dump(exclude_unset=True)
    print(data)

    for key, value in data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh
    return obj

def delete_patient(db: Session, patiend_id: int) -> None:
    obj = get_patient(db, patiend_id)
    db.delete(obj) 
    db.commit()