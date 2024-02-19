from agendfy import config
from agendfy.models import models
from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime, timezone
from fastapi import Depends
from typing import Annotated


def engine () -> create_engine:
    return create_engine(config.database_url, echo=True)

def yield_session ():
    with Session(engine()) as session:
        yield session

def migrate () -> None:
    SQLModel.metadata.create_all(engine())

def seed () -> None:
    with Session(engine()) as db:
        if db.get(models.Appointment, 1):
            return
        company_1 = models.Company(
            name="Company 1",
            description="Company 1 description",
            cpf="41756250898",
            phone="11999999999",
        )
        db.add(company_1)
        db.commit()
        db.refresh(company_1)

        user_1 = models.User(
            email="email@email.com",
            password="password",
            company_id=company_1.id,
        )
        db.add(user_1)
        db.commit()
        db.refresh(user_1)

        service = models.Service(
            name="Troca de óleo - Veículo Grande",
            description="Troca de óleo de veículo",
            amount=10.0,
            company_id=company_1.id,
        )
        service_2 = models.Service(
            name="Troca de pneu", 
            description="Troca de pneu de veículo", 
            amount=20.0,
            company_id=company_1.id,
        )
        db.add(service)
        db.add(service_2)
        appointment = models.Appointment(
            title="Schendule to car",
            start=datetime.now(timezone.utc),
            end=datetime.now(timezone.utc),
            user_id=user_1.id,
        )
        db.add(appointment)
        # Todo, achar uma forma de não precisar fazer o commit aqui
        db.commit()
        db.refresh(appointment)
        db.refresh(service)
        db.refresh(service_2)
        appointment_services = models.AppointmentServices(
            appointment_id=appointment.id, service_id=service.id, quantity=1
        )
        appointment_services_2 = models.AppointmentServices(
            appointment_id=appointment.id, service_id=service_2.id, quantity=2
        )
        db.add(appointment_services)
        db.add(appointment_services_2)
        db.commit()


DatabaseDepends = Annotated[Session, Depends(yield_session)]
