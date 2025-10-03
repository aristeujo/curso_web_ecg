from datetime import date, time
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Field, model_validator
from pydantic.config import ConfigDict
from pydantic.functional_validators import BeforeValidator

from backend.app.utils.validators import validate_pressure, unify_pressure_payload, SYS_MIN, SYS_MAX, DIA_MAX, DIA_MIN

PressureCanon = Annotated[str, BeforeValidator(validate_pressure)]

class TriageBase(BaseModel):
    patient_id: int = Field(..., ge = 1, description = "ID do paciente")
    triage_date: date = Field(..., description = "Data da triagem")
    triage_time: time = Field(..., descritpion = "Hora da Triagem")
    weight_kg: float = Field(..., gt=0, le=500, descritption = "Peso em Kg")
    height_cm: float = Field(..., gt=20, le=300, descritption = "Altura em cm")
    glucose_mg_dl: float = Field(..., ge=0, le=1000, descritption = "Glicemia capilar (mg/dL)")
    heart_rate_bpm: int = Field(..., gt=20, le=250, descritption = "Frequência cardíaca (bpm)")
    pressure: PressureCanon = Field(..., description="Pressão arterial em mmHg; ex: 120/80")
    fasting: bool = Field(...,description="Se o paciente estava em jejum")
    notes: Optional[str] = Field(None, max_length=2000)

class TriageCreate(TriageBase):
    systolic_mmHg: Optional[int] = Field(None, ge=SYS_MIN, le=SYS_MAX)
    diastolic_mmHg: Optional[int] = Field(None, ge=DIA_MIN, le=DIA_MAX)

    @model_validator(mode="before")
    @classmethod
    def _unify_pressure(cls, data):
        return unify_pressure_payload(data)
    
class TriageOut(TriageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int