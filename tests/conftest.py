import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Must set env vars before importing app modules
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test_db")
os.environ.setdefault("OPENAI_API_KEY", "fake-key-for-tests")
os.environ.setdefault("JWT_SECRET", "test-secret")

from app.database import Base, get_db
from app.main import app
from app.models import Word, Situation, SituationWord


engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables once per test session, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Provide a transactional database session that rolls back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    """FastAPI test client with DB session override."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def seed_data(db):
    """Insert minimal reference data: words, situations, situation_words."""
    # Encounter words
    encounter_words = [
        Word(id="enc_1", spanish="cuenta", english="account", word_category="encounter"),
        Word(id="enc_2", spanish="depositar", english="to deposit", word_category="encounter"),
        Word(id="enc_3", spanish="retirar", english="to withdraw", word_category="encounter"),
        Word(id="enc_4", spanish="mesa", english="table", word_category="encounter"),
        Word(id="enc_5", spanish="menu", english="menu", word_category="encounter"),
        Word(id="enc_6", spanish="propina", english="tip", word_category="encounter"),
    ]
    # High frequency words
    high_freq_words = [
        Word(id="hf_1", spanish="hola", english="hello", word_category="high_frequency", frequency_rank=1),
        Word(id="hf_2", spanish="gracias", english="thank you", word_category="high_frequency", frequency_rank=2),
        Word(id="hf_3", spanish="por favor", english="please", word_category="high_frequency", frequency_rank=3),
    ]
    for w in encounter_words + high_freq_words:
        db.add(w)

    # Situations
    situations = [
        Situation(id="bank_open_1", title="Opening a Bank Account", animation_type="banking", encounter_number=1, order_index=1, is_free=True),
        Situation(id="bank_wire_1", title="Wire Transfer", animation_type="banking", encounter_number=1, order_index=2, is_free=False),
        Situation(id="rest_order_1", title="Ordering Food", animation_type="restaurant", encounter_number=1, order_index=3, is_free=True),
    ]
    for s in situations:
        db.add(s)

    # Link encounter words to situations
    situation_words = [
        SituationWord(situation_id="bank_open_1", word_id="enc_1", position=1),
        SituationWord(situation_id="bank_open_1", word_id="enc_2", position=2),
        SituationWord(situation_id="bank_open_1", word_id="enc_3", position=3),
        SituationWord(situation_id="rest_order_1", word_id="enc_4", position=1),
        SituationWord(situation_id="rest_order_1", word_id="enc_5", position=2),
        SituationWord(situation_id="rest_order_1", word_id="enc_6", position=3),
    ]
    for sw in situation_words:
        db.add(sw)

    db.flush()
    return {
        "encounter_words": encounter_words,
        "high_freq_words": high_freq_words,
        "situations": situations,
    }


def register_user(client, email="test@example.com", password="testpassword123"):
    """Helper: register a user and return (response_json, auth_headers)."""
    resp = client.post("/v1/auth/register", json={
        "email": email,
        "password": password,
        "confirm_password": password,
    })
    data = resp.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    return data, headers


@pytest.fixture
def auth_user(client):
    """Register a test user and return (user_data, auth_headers)."""
    return register_user(client)
