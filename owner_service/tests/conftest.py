import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from owner_service import database
from owner_service.main import app as owner_app, get_db as get_owner_db

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # or sqlite:///:memory:
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure test DB tables are created
database.Base.metadata.create_all(bind=database.engine)

# Dependency override
def override_get_test_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply DB override for owner service
test_owner_app = owner_app
test_owner_app.dependency_overrides[get_owner_db] = override_get_test_db


@pytest.fixture(scope="module")
def owner_client():
    return TestClient(test_owner_app)