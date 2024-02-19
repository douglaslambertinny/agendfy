from agendfy.database import DatabaseDepends
from agendfy.models import models
from fastapi import APIRouter
from http import HTTPStatus
from sqlmodel import select
from typing import List

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
    )

class AppointmentCreate(models.AppointmentBase):
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": 1,
                "user_id": 1,
                "start": "2021-08-01T00:00:00",
                "end": "2021-08-01T01:00:00",
                "description": "Appointment Test",
            }
        }

class AppointmentRead(models.ModelId, models.AppointmentBase):
    item_service_links: List[models.AppointmentServices] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "company_id": 1,
                "user_id": 1,
                "start": "2021-08-01T00:00:00",
                "end": "2021-08-01T01:00:00",
                "description": "Appointment Test",
                "created_at": "2021-08-01T00:00:00",
                "updated_at": "2021-08-01T00:00:00",
                "deleted_at": None,
            }
        }


@router.get("", response_model=List[AppointmentRead], status_code=HTTPStatus.OK)
def get_appointments(db: DatabaseDepends):
    query = select(models.Appointment).where(models.Appointment.deleted_at == None)
    return db.exec(query).all()


@router.get("/{id}", response_model=AppointmentRead, status_code=HTTPStatus.OK)
def get_appointment(db: DatabaseDepends, appointment_id: int):
    query = select(models.Appointment).where(models.Appointment.id == appointment_id)
    return db.exec(query).first()


@router.post("", response_model=AppointmentRead, status_code=HTTPStatus.CREATED)
def create_appointment(db: DatabaseDepends, appointment: AppointmentCreate):
    appointment_to_db = models.Appointment.model_validate(appointment)
    db.add(appointment_to_db)
    db.commit()
    db.refresh(appointment_to_db)
    return appointment_to_db
