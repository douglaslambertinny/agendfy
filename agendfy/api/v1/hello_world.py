from fastapi import APIRouter


router = APIRouter(
    prefix="/hello-world",
    tags=["Hello World"],
)

@router.get("/")
def hello_world():
    return {"message": "Hello World!"}