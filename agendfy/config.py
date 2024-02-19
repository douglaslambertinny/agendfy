from os import environ

database_url = environ.get("DATABASE_URL", "sqlite:///agendfy.db")
port = int(environ.get("PORT", 5500))
debug = bool(environ.get("DEBUG", True))