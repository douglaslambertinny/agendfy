from agendfy.api import v1
from agendfy.database import database
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastui import prebuilt_html


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup/teardown routine.
    """
    
    database.migrate()
    database.seed()

    yield


app = FastAPI(title="AgendFy API", version="1.0.0", lifespan=lifespan)
@app.get("/{path:path}")
def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo", api_root_url="/v1"))

app.include_router(v1.router)
