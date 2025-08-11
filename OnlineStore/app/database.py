# Database engine and session setup
from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./app.db"  # Use "sqlite:///:memory:" for in-memory

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
