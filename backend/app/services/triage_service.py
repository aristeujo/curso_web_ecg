from datetime import datetime, timedelta, timezone
from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from sqlalchemy import desc

from backend.app.db_models import Patient, Triage
from backend.app.models.triage import TriageCreate

def _triage_has_columns(*names: str) -> bool:
    cols = set(inspect(Triage).columns.keys())
    return set(names).issubset(cols)


def _combine_dt(triage: Triage) -> Optional[datetime]:
    if _triage_has_columns("created_at"):
        created = getattr(triage, "created_at", None)
        if created is not None:
            return created

    if _triage_has_columns("triage_date", "triage_time"):
        td = getattr(triage, "triage_date", None)
        tt = getattr(triage, "triage_time", None)
        if isinstance(td, date) and isinstance(tt, dtime):
            return datetime.combine(td, tt)

    return None

def has_recent_triage(db: Session, patient_id: int, minutes: int = 3) -> bool:
    q = db.query(Triage).filter(Triage.patient_id == patient_id)

    if _triage_has_columns("created_at"):
        q = q.order_by(desc(getattr(Triage, "created_at")))
    elif _triage_has_columns("triage_date", "triage_time"):
        q = q.order_by(
            desc(getattr(Triage, "triage_date")),
            desc(getattr(Triage, "triage_time")),
        )
    else:
        q = q.order_by(desc(Triage.id))

    last = q.first()
    if not last:
        return False

    last_dt = _combine_dt(last)
    if not last_dt:
        return False

    return datetime.now(timezone.utc) - last_dt <= timedelta(minutes=minutes)

def create_triage(db: Session, payload: TriageCreate) -> Triage:
    patient = db.get(Patient, payload.patient_id)

    if not patient:
        raise ValueError("patient-not-found")

    if has_recent_triage(db, payload.patient_id):
        raise ValueError("triage-recent-conflict")

    triage_time_str = payload.triage_time.strftime("%H:%M")

    if payload.systolic_mmHg is not None and payload.diastolic_mmHg is not None:
        pressure_str = f"{payload.systolic_mmHg}/{payload.diastolic_mmHg}"
    else:
        pressure_str = str(payload.pressure)

    data = payload.model_dump(
        exclude_unset=True,
        exclude={"systolic_mmHg", "diastolic_mmHg", "triage_time", "pressure"},
    )
    data["triage_time"] = triage_time_str
    data["pressure"] = pressure_str

    obj = Triage(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj   

def get_triage(db: Session, triage_id: int) -> Triage:
    obj = db.query(Triage).filter(Triage.id == triage_id).first()
    if not obj:
        raise ValueError("triage-not-found")
    return obj


def list_triages(
    db: Session,
    patient_id: Optional[int] = None,
    page: int = 1,
    size: int = 50,
) -> List[Triage]:
    q = db.query(Triage)
    if patient_id is not None:
        q = q.filter(Triage.patient_id == patient_id)

    if _triage_has_columns("triage_date", "triage_time"):
        q = q.order_by(
            desc(getattr(Triage, "triage_date")),
            desc(getattr(Triage, "triage_time")),
        )
    elif _triage_has_columns("created_at"):
        q = q.order_by(desc(getattr(Triage, "created_at")))
    else:
        q = q.order_by(desc(Triage.id))

    return q.offset((page - 1) * size).limit(size).all()



def delete_triage(db: Session, triage_id: int) -> None:
    obj = get_triage(db, triage_id)
    db.delete(obj)
    db.commit()
