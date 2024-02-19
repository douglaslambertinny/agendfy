from agendfy.api import v1
from agendfy.database import database
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup/teardown routine.
    """
    
    database.migrate()
    database.seed()

    yield


app = FastAPI(title="AgendFy API", version="1.0.0", lifespan=lifespan)
app.include_router(v1.router)
