from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS  # Импортируем CORS
from flask_jwt_extended import JWTManager, create_access_token
from database import create_db_engine, create_session
from models import Base, User

app = Flask(__name__)
api = Api(app, doc='/documentation')

# Разрешаем CORS для http://localhost:3000
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Разрешение только для этого домена

# Настройка секретного ключа для JWT (замените на более безопасный ключ)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  
jwt = JWTManager(app)  # Инициализация JWT

# Создаем подключение к базе данных
engine = create_db_engine()
Base.metadata.create_all(engine)

# Модели для регистрации и ошибки остаются такими же, как в вашем примере

# Модель для регистрации
signup_model = api.model(
    'SignUpModel', {
        "first_name": fields.String(required=True, min_length=2, max_length=32, description="Имя пользователя"),
        "last_name": fields.String(required=True, min_length=2, max_length=32, description="Фамилия пользователя"),
        "login": fields.String(required=True, min_length=2, max_length=32, description="Логин для входа"),
        "password": fields.String(required=True, min_length=4, max_length=16, description="Пароль для входа"),
        "mail": fields.String(required=True, min_length=4, max_length=64, description="Электронная почта пользователя")
    }
)

# Модель для успешного ответа при регистрации
success_response = api.model(
    'SuccessResponse', {
        "success": fields.Boolean(description="Успешность операции"),
        "userID": fields.Integer(description="ID зарегистрированного пользователя"),
        "msg": fields.String(description="Сообщение о статусе регистрации")
    }
)

# Модель для ошибки
error_response = api.model(
    'ErrorResponse', {
        "success": fields.Boolean(description="Успешность операции"),
        "msg": fields.String(description="Сообщение об ошибке")
    }
)

# Модель для входа
login_model = api.model(
    'LoginModel', {
        "login": fields.String(required=True, min_length=2, max_length=32, description="Логин пользователя"),
        "password": fields.String(required=True, min_length=4, max_length=16, description="Пароль пользователя")
    }
)

# Модель для успешного ответа при входе
login_success_response = api.model(
    'LoginSuccessResponse', {
        "success": fields.Boolean(description="Успешность операции"),
        "msg": fields.String(description="Сообщение о статусе входа"),
        "access_token": fields.String(description="Токен для доступа")
    }
)

# Модель для ошибки входа
login_error_response = api.model(
    'LoginErrorResponse', {
        "success": fields.Boolean(description="Успешность операции"),
        "msg": fields.String(description="Сообщение об ошибке")
    }
)

# Ресурс для регистрации пользователя
@api.route('/api/users/register')
class Register(Resource):
    @api.expect(signup_model, validate=True)
    @api.response(201, 'Пользователь успешно зарегистрирован', model=success_response)
    @api.response(400, 'Пользователь с таким логином или email уже существует', model=error_response)
    @api.response(500, 'Внутренняя ошибка сервера', model=error_response)
    @api.doc(description="Регистрация нового пользователя")
    def post(self):
        """Регистрирует нового пользователя"""
        req_data = request.get_json()

        session = create_session(engine)
        try:
            # Проверка на наличие пользователя с таким логином или email
            existing_user = session.query(User).filter(
                (User.login == req_data["login"]) | (User.mail == req_data["mail"])
            ).first()

            if existing_user:
                return {"success": False, "msg": "Пользователь с таким логином или email уже существует"}, 400

            # Создание нового пользователя
            new_user = User(
                first_name=req_data["first_name"],
                last_name=req_data["last_name"],
                login=req_data["login"],
                mail=req_data["mail"]
            )
            new_user.set_password(req_data["password"])  # Устанавливаем хэш пароля

            # Сохраняем пользователя в базе
            session.add(new_user)
            session.commit()

            session.refresh(new_user)  # Получаем ID нового пользователя

            return {
                "success": True,
                "userID": new_user.id,
                "msg": "Пользователь успешно зарегистрирован"
            }, 201

        except Exception as e:
            session.rollback()
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()

# Ресурс для входа пользователя
@api.route('/api/users/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Пользователь успешно авторизован', model=login_success_response)
    @api.response(401, 'Неверный логин или пароль', model=login_error_response)
    @api.doc(description="Авторизация пользователя с использованием логина и пароля")
    def post(self):
        """Авторизация пользователя"""
        req_data = request.get_json()

        session = create_session(engine)
        try:
            # Поиск пользователя в базе данных по логину
            user = session.query(User).filter(User.login == req_data["login"]).first()

            if not user or not user.check_password(req_data["password"]):
                return {"success": False, "msg": "Неверный логин или пароль"}, 401

            # Если логин и пароль верные, создаем токен доступа
            access_token = create_access_token(identity=user.id)

            return {
                "success": True,
                "msg": "Пользователь успешно авторизован",
                "access_token": access_token
            }, 200

        except Exception as e:
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()

if __name__ == '__main__':
    app.run(debug=True)
