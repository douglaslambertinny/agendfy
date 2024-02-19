from pytest import fixture
from fastapi.testclient import TestClient
from agendfy.app import app
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from agendfy.database import yield_session

engine = create_engine(
    "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
)
client = TestClient(app)


def override_yield_session():
    """
    Use test database.
    """

    with Session(engine) as session:
        yield session


app.dependency_overrides[yield_session] = override_yield_session


@fixture(autouse=True)
def db():
    """
    Recreate database and yield session for every test case.
    """

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)
