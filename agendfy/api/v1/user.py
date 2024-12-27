from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from agendfy.database import DatabaseDepends
from agendfy.models import models
from sqlmodel import SQLModel
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui import events

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

class UserCreate(models.UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "User Test",
                "email": "usertest@example.com",
                "password": "password",
                "company_id": 1,
            }
        }

class UserRead(models.UserBase, SQLModel):
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "User Test",
                "email": "usertest@example.com",
                "created_at": "2021-08-01T00:00:00",
                "updated_at": "2021-08-01T00:00:00",
                "deleted_at": None,
            }
        }


# @router.post("", response_model=UserRead)
# def post(db: DatabaseDepends, user: UserCreate):
#     user_to_db = models.User.model_validate(user)
#     db.add(user_to_db)
#     db.commit()
#     db.refresh(user_to_db)
#     return user_to_db


# @router.get("", response_model=UserRead)
# def get_all(db: DatabaseDepends):
#     query = models.User.select()
#     return db.exec(query).all()


# @router.get("/{user_id}", response_model=UserRead)
# def get(db: DatabaseDepends, user_id: int):
#     query = models.User.select().where(models.User.id == user_id)
#     return db.exec(query).first()


@router.get(
    "/{user_id}", response_model=FastUI, response_model_exclude_none=True
)
def interface(db: DatabaseDepends, user_id: int):
    query = models.User.select().where(models.User.id == user_id)
    user = db.exec(query).first()
    return [
        c.Page(
            components=[
                c.Heading(text=user.email, level=2),
                c.Link(components=[c.Text(text="Back")], on_click=events.BackEvent()),
                c.Details(data=user),
            ]
        ),
    ]
