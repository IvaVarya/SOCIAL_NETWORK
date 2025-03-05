#app.py
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from database import create_db_engine, create_session
from models import Profile, Base
from schemas import ProfileSchema
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
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Указываем, где искать токен (в заголовках)
app.config['JWT_HEADER_NAME'] = 'Authorization'  # Имя заголовка для токена
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # Тип токена

jwt = JWTManager(app)

# Создаем engine для подключения к базе данных
engine = create_db_engine()

# Модели для Swagger
profile_model = api.model('ProfileModel', {
    "first_name": fields.String(required=False),
    "last_name": fields.String(required=False),
    "gender": fields.String(required=False),
    "date_of_birth": fields.String(required=False),
    "country": fields.String(required=False),
    "city": fields.String(required=False),
    "profile_picture": fields.String(required=False),
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

@api.route('/profile')
class ProfileResource(Resource):
    @jwt_required()
    @api.expect(profile_model)
    def put(self):
        user_id = get_jwt_identity()
        req_data = request.get_json()
        schema = ProfileSchema()
        errors = schema.validate(req_data)
        if errors:
            return {"success": False, "msg": "Invalid data", "errors": errors}, 400

        session = create_session(engine)
        try:
            profile = session.query(Profile).filter(Profile.user_id == user_id).first()
            if not profile:
                profile = Profile(user_id=user_id)
                session.add(profile)
            
            # Обновляем только те поля, которые переданы в запросе
            for key, value in req_data.items():
                if value is not None:  # Обновляем только если значение передано
                    setattr(profile, key, value)
            
            session.commit()
            return {"success": True, "msg": "Профиль успешно обновлен"}, 200
        except Exception as e:
            session.rollback()
            logger.error("Error updating profile", error=str(e))
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()

    @jwt_required()
    @api.expect(profile_model)
    def put(self):
        user_id = get_jwt_identity()
        req_data = request.get_json()
        schema = ProfileSchema()
        errors = schema.validate(req_data)
        if errors:
            return {"success": False, "msg": "Invalid data", "errors": errors}, 400

        session = create_session(engine)
        try:
            profile = session.query(Profile).filter(Profile.user_id == user_id).first()
            if not profile:
                profile = Profile(user_id=user_id)
                session.add(profile)
            
            for key, value in req_data.items():
                setattr(profile, key, value)
            
            session.commit()
            return {"success": True, "msg": "Профиль успешно обновлен"}, 200
        except Exception as e:
            session.rollback()
            logger.error("Error updating profile", error=str(e))
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)