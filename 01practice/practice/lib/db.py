from sqlmodel import Session, create_engine

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
