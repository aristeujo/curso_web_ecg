from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.models.patient import PatientCreate, PatientUpdate, PatientOut
from backend.app.services.patient_service import create_patient, list_patients, update_patient, get_patient, search_patients_by_name, delete_patient

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("", response_model=PatientOut, status_code = status.HTTP_201_CREATED)
def create_patient_route(payload: PatientCreate, db: Session = Depends(get_db)):
    try:
        return create_patient(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email ou telefone ja cadastrado")
    
@router.get("/search", response_model=List[PatientOut])
def search_patient_by_name_route(
    q: str = Query(..., min_length=2, description="Nome (ou parte) do paciente"),
    db: Session = Depends(get_db),
):
    return search_patients_by_name(db, q)

@router.get("/{patient_id}", response_model=PatientOut)
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    try:
        return get_patient(db, patient_id)
    except ValueError as e:
        if str(e) == "patient-not-found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        raise

@router.get("/", response_model=List[PatientOut])
@router.get("", response_model=List[PatientOut], include_in_schema=False) 
def list_patients_route(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return list_patients(db, page, size)

@router.put("/{patient_id}", response_model=PatientOut)
def update_patient_route(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    try:
        return update_patient(db, patient_id, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email ou telefone já cadastrado")
    except ValueError as e:
        msg = str(e)
        if msg == "patient-not-found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        if msg == "patient-conflict":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Paciente já cadastrado")
        raise


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    try:
        delete_patient(db, patient_id)
        return None
    except ValueError as e:
        if str(e) == "patient-not-found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        raise
