from agendfy.database import DatabaseDepends
from agendfy.models import models
from fastapi import APIRouter
from sqlmodel import select
from http import HTTPStatus
from typing import List

router = APIRouter(prefix="/companies", tags=["Company"])


class CompanyCreate(models.CompanyBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Company Test",
                "cnpj": "912898329389238",
                "cpf": "41756250898",
                "phone": "11966325206",
            }
        }


class CompanyRead(models.ModelId, models.ModelTimeStamps, models.CompanyBase):
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Company Test",
                "created_at": "2021-08-01T00:00:00",
                "updated_at": "2021-08-01T00:00:00",
                "deleted_at": None,
                "cnpj": "912898329389238",
                "cpf": "41756250898",
                "phone": "11966325206",
            }
        }


@router.post("", response_model=CompanyRead, status_code=HTTPStatus.CREATED)
def post(db: DatabaseDepends, company: CompanyCreate):
    company_to_db = models.Company.model_validate(company)
    db.add(company_to_db)
    db.commit()
    db.refresh(company_to_db)
    return company_to_db

@router.get("", response_model=List[CompanyRead], status_code=HTTPStatus.OK)
def search(db: DatabaseDepends):
    query = select(models.Company).where(models.Company.deleted_at == None)
    return db.exec(query).all()

@router.get("/{company_id}", response_model=CompanyRead, status_code=HTTPStatus.OK)
def get(db: DatabaseDepends, company_id: int):
    query = select(models.Company).where(models.Company.id == company_id)
    return db.exec(query).first()
