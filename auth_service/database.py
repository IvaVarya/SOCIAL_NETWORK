#database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os

logger = logging.getLogger(__name__)

def create_db_engine():
    db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:mars@postgres:5432/SOCIAL_NETWORK')
    logger.debug(f"Creating engine with URL: {db_url}")
    return create_engine(db_url)

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()