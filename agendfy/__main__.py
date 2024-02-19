import uvicorn
from agendfy import config

uvicorn.run(
        "agendfy.app:app",
        host="0.0.0.0",
        port=config.port,
        reload=config.debug,
)