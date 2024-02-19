from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List

class ModelBase(SQLModel):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        """Set table name to snake case"""
        table_name = "".join(["_" + i.lower() if i.isupper() else i for i in cls.__name__]).lstrip("_")
        cls.__tablename__ = table_name

class ModelTimeStamps(ModelBase):
    """Base class to add timestamps to models."""
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    deleted_at: Optional[datetime] = None

class ModelId(SQLModel):
    """Base class to add id to models."""

    id: int = Field(default=None, primary_key=True)

# Services
class ServiceBase(ModelBase):
    name: str
    description: Optional[str] = None
    amount: float = Field(default=0.0)


class Service(ModelId, ModelTimeStamps, ServiceBase, table=True):
    company_id: int = Field(default=None, foreign_key="company.id")
    item_appointment_links: List["AppointmentServices"] = Relationship(
        back_populates="service"
    )


# Lines with services in appointment
class AppointmentServices(ModelBase, table=True):
    appointment_id: int = Field(
        default=None, foreign_key="appointment.id", primary_key=True
    )
    service_id: int = Field(default=None, foreign_key="service.id", primary_key=True)
    quantity: int = Field(default=1)
    appointment: "Appointment" = Relationship(back_populates="item_service_links")
    service: "Service" = Relationship(back_populates="item_appointment_links")


# Appointment
class AppointmentBase(ModelBase): 
    title: str
    description: Optional[str] = None
    start: datetime
    end: datetime
    user_id: int = Field(default=None, foreign_key="user.id")


class Appointment(ModelId, ModelTimeStamps, AppointmentBase, table=True):
    item_service_links: List["AppointmentServices"] = Relationship(back_populates="appointment")


# Company
class CompanyBase(ModelBase):
    name: str
    cnpj: Optional[str] = None
    cpf: str = None
    phone: str


class Company(ModelId, ModelTimeStamps, CompanyBase, table=True):
    users: Optional[List["User"]] = Relationship(back_populates="company")


# User
class UserBase(ModelBase):
    email: str
    password: str


class User(ModelId, ModelTimeStamps, UserBase, table=True):
    company_id: int = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="users")
