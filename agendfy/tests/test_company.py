from . import db, client
from agendfy.models import models

def test_post_company():

    response = client.post(
        "/v1/companies",
        json={
            "name": "Company Test",
            "cnpj": "912898329389238",
            "cpf": "41756250898",
            "phone": "11966325206",
        },
    )
    assert response.status_code == 201

def test_search_companies(db):
    company_1 = models.Company(name="Company Test", cnpj="912898329389238", cpf="41756250898", phone="11966325206")
    company_2 = models.Company(name="Company Test 2", cnpj="912898329389238", cpf="41756250898", phone="11966325206")
    db.add(company_1)
    db.add(company_2)
    db.commit()
    db.refresh(company_1)
    db.refresh(company_2)

    response = client.get("/v1/companies")
    assert response.status_code == 200

