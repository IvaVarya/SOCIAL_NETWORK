#app.py
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token
from flask_caching import Cache
from database import create_db_engine, create_session
from models import User
from schemas import UserSchema
from prometheus_client import start_http_server, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import structlog
import time
import os
from alembic import command
from alembic.config import Config

# Применение миграций
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

# Настройка structlog для логирования
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    wrapper_class=structlog.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = Flask(__name__)
api = Api(app)

# Конфигурация JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback_secret_key')
jwt = JWTManager(app)

# Конфигурация кэширования Redis
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = os.getenv('REDIS_URL', 'redis://redis:6379/0')
cache = Cache(app)

# Создаем engine для подключения к базе данных
engine = create_db_engine()

# Модели для Swagger
signup_model = api.model('SignUpModel', {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "login": fields.String(required=True),
    "password": fields.String(required=True),
    "confirm_password": fields.String(required=True),
    "mail": fields.String(required=True)
})

login_model = api.model('LoginModel', {
    "login": fields.String(required=True),
    "password": fields.String(required=True)
})

# Prometheus метрики
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency in seconds')

@app.before_request
def before_request():
    request.start_time = time.time()
    logger.info("Request started", path=request.path)

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(latency)
    logger.info("Request completed", path=request.path, latency=latency)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@api.route('/register')
class Register(Resource):
    @api.expect(signup_model)
    def post(self):
        req_data = request.get_json()
        schema = UserSchema()
        errors = schema.validate(req_data)
        if errors:
            return {"success": False, "msg": "Invalid data", "errors": errors}, 400

        session = create_session(engine)
        try:
            existing_user = session.query(User).filter(
                (User.login == req_data["login"]) | (User.mail == req_data["mail"])
            ).first()
            if existing_user:
                return {"success": False, "msg": "Пользователь с таким логином или email уже существует"}, 400

            new_user = User(
                first_name=req_data["first_name"],
                last_name=req_data["last_name"],
                login=req_data["login"],
                mail=req_data["mail"]
            )
            new_user.set_password(req_data["password"])
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return {"success": True, "userID": new_user.id, "msg": "Пользователь успешно зарегистрирован"}, 201
        except Exception as e:
            session.rollback()
            logger.error("Error during registration", error=str(e))
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        req_data = request.get_json()
        session = create_session(engine)
        try:
            user = session.query(User).filter(User.login == req_data["login"]).first()
            if not user or not user.check_password(req_data["password"]):
                return {"success": False, "msg": "Неверный логин или пароль"}, 401
            access_token = create_access_token(identity=str(user.id))  # Преобразуем user.id в строку
            return {"success": True, "msg": "Пользователь успешно авторизован", "access_token": access_token}, 200
        except Exception as e:
            logger.error("Error during login", error=str(e))
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)