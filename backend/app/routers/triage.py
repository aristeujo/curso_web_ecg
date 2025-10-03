from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.triage import TriageCreate, TriageOut
from backend.app.services.triage_service import (
    create_triage,
    get_triage,
    list_triages,
    delete_triage,
)

router = APIRouter(prefix="/triages", tags=["triages"])

@router.post("/", response_model=TriageOut, status_code=status.HTTP_201_CREATED)
def create_triage_route(payload: TriageCreate, db: Session = Depends(get_db)):
    try:
        return create_triage(db, payload)
    except ValueError as e:
        msg = str(e)
        if msg == "paciente nao encontrado":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
        if msg == "Conflito na triagem":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Triagem recente já registrada para este paciente.")
        raise


@router.get("/", response_model=List[TriageOut])
def list_triages_route(
    patient_id: Optional[int] = Query(None, ge=1),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return list_triages(db, patient_id, page, size)


@router.get("/{triage_id}", response_model=TriageOut)
def get_triage_route(triage_id: int, db: Session = Depends(get_db)):
    try:
        return get_triage(db, triage_id)
    except ValueError as e:
        if str(e) == "triage-not-found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Triagem não encontrada")
        raise

@router.delete("/{triage_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_triage_route(triage_id: int, db: Session = Depends(get_db)):
    try:
        delete_triage(db, triage_id)
        return None
    except ValueError as e:
        if str(e) == "triage-not-found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Triagem não encontrada")
        raise
