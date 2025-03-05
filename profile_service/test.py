#test.py
import pytest
from app import app
from models import Profile
from database import create_db_engine

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_profile(client):
    response = client.get('/profile')
    assert response.status_code == 401  # Неавторизованный доступ

def test_update_profile(client):
    response = client.put('/profile', json={
        "first_name": "Иван",
        "last_name": "Иванов",
        "gender": "Мужской",
        "date_of_birth": "1990-01-01",
        "country": "Россия",
        "city": "Москва"
    })
    assert response.status_code == 401  # Неавторизованный доступ