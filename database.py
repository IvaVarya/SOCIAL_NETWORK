#database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db_engine():
    username = 'postgres'
    password = 'mars'
    host = 'localhost'
    port = '5432'
    database = 'SOCIAL_NETWORK'

    db_url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(db_url)

    return engine

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
