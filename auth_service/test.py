#test.py
import pytest
from app import app
from models import User
from database import create_db_engine
from schemas import UserSchema

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_valid_data(client):
    response = client.post('/register', json={
        "first_name": "Иван",
        "last_name": "Иванов",
        "login": "ivan123",
        "password": "pass123",
        "confirm_password": "pass123",
        "mail": "ivan@example.com"
    })
    assert response.status_code == 201
    assert response.json['success'] is True

def test_register_invalid_first_name(client):
    response = client.post('/register', json={
        "first_name": "иван",  # Начинается с маленькой буквы
        "last_name": "Иванов",
        "login": "ivan123",
        "password": "pass123",
        "confirm_password": "pass123",
        "mail": "ivan@example.com"
    })
    assert response.status_code == 400
    assert "Имя должно начинаться с заглавной буквы" in response.json['errors']['first_name']

def test_register_invalid_login(client):
    response = client.post('/register', json={
        "first_name": "Иван",
        "last_name": "Иванов",
        "login": "ivan@123",  # Недопустимые символы
        "password": "pass123",
        "confirm_password": "pass123",
        "mail": "ivan@example.com"
    })
    assert response.status_code == 400
    assert "Логин должен содержать только латинские буквы" in response.json['errors']['login']

def test_register_invalid_password(client):
    response = client.post('/register', json={
        "first_name": "Иван",
        "last_name": "Иванов",
        "login": "ivan123",
        "password": "pass",  # Меньше 6 символов
        "confirm_password": "pass",
        "mail": "ivan@example.com"
    })
    assert response.status_code == 400
    assert "Пароль должен содержать минимум 6 символов" in response.json['errors']['password']

def test_register_passwords_not_match(client):
    response = client.post('/register', json={
        "first_name": "Иван",
        "last_name": "Иванов",
        "login": "ivan123",
        "password": "pass123",
        "confirm_password": "pass1234",  # Пароли не совпадают
        "mail": "ivan@example.com"
    })
    assert response.status_code == 400
    assert "Пароли не совпадают" in response.json['errors']['confirm_password']