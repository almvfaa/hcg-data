from backend.db.session import SessionLocal

def get_db():
    """
    Dependency function to get a database session.
    This should be used with FastAPI's dependency injection system.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
