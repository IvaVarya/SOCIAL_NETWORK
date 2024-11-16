from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS  # Импортируем CORS
from database import create_db_engine, create_session
from models import Base, User

app = Flask(__name__)
api = Api(app, doc='/documentation')  # URL для Swagger документации

# Отключаем CORS (не настраиваем для разрешения запросов)
CORS(app, resources={r"/*": {"origins": "*"}})  # Это строка отключает CORS для всех ресурсов

# Создаем подключение к базе данных
engine = create_db_engine()
Base.metadata.create_all(engine)  # Создаем таблицы

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

# Модель для ответа при запросе профиля пользователя
user_profile_model = api.model(
    'UserProfile', {
        "id": fields.Integer(description="ID пользователя"),
        "first_name": fields.String(description="Имя пользователя"),
        "last_name": fields.String(description="Фамилия пользователя"),
        "login": fields.String(description="Логин"),
        "mail": fields.String(description="Электронная почта")
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


# Ресурс для получения данных пользователя
@api.route('/api/users/<int:user_id>')
class UserProfile(Resource):
    @api.response(200, 'Информация о пользователе успешно получена', model=user_profile_model)
    @api.response(404, 'Пользователь не найден', model=error_response)
    @api.response(500, 'Внутренняя ошибка сервера', model=error_response)
    @api.doc(description="Получение информации о пользователе по ID")
    def get(self, user_id):
        """Возвращает информацию о пользователе по ID"""
        session = create_session(engine)
        try:
            # Поиск пользователя в базе данных
            user = session.query(User).filter(User.id == user_id).first()

            if not user:
                return {"success": False, "msg": "Пользователь не найден"}, 404

            # Формируем ответ с данными пользователя
            return {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "login": user.login,
                "mail": user.mail
            }, 200

        except Exception as e:
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()


if __name__ == '__main__':
    app.run(debug=True)
