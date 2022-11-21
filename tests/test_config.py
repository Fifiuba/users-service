from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from users_service.database import models, database
from users_service.utils.events_handler import get_event
from users_service.utils.events_mockup import EventsMock
from users_service.utils.firebase_mock import FirebaseMock
from users_service.utils.firebase_handler import get_fb


session = None

# database
def init_database(app):

    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[database.get_db] = override_get_db
    return TestingSessionLocal()

def init_events(app):
    events = EventsMock()

    def override_get_events():
        try:
            yield events
        finally:
            events

    app.dependency_overrides[get_event] = override_get_events

# firebase
def init_firebase(app):
    firebase = FirebaseMock()

    def override_get_fb():
        try:
            yield firebase
        finally:
            firebase

    app.dependency_overrides[get_fb] = override_get_fb
