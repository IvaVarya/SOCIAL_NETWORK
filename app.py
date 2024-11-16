from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from database import create_db_engine, create_session
from models import Base, User

app = Flask(__name__)
api = Api(app, doc='/documentation')  # URL для Swagger документации

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

# Модель для успешного ответа
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

        # Создаем сессию для работы с БД
        session = create_session(engine)
        try:
            # Проверка на наличие пользователя с тем же логином или email
            existing_user = session.query(User).filter(
                (User.login == req_data["login"]) | (User.mail == req_data["mail"])
            ).first()

            if existing_user:
                return {"success": False, "msg": "Пользователь с таким логином или email уже существует"}, 400

            # Создаем нового пользователя
            new_user = User(
                first_name=req_data["first_name"],
                last_name=req_data["last_name"],
                login=req_data["login"],
                mail=req_data["mail"]
            )
            new_user.set_password(req_data["password"])  # Устанавливаем хэш пароля

            # Добавляем пользователя в сессию и коммитим изменения
            session.add(new_user)
            session.commit()

            # Обновляем объект после коммита, чтобы получить его id
            session.refresh(new_user)

            return {
                "success": True,
                "userID": new_user.id,
                "msg": "Пользователь успешно зарегистрирован"
            }, 201

        except Exception as e:
            session.rollback()  # В случае ошибки откатываем изменения
            return {"success": False, "msg": str(e)}, 500
        finally:
            session.close()  # Закрываем сессию

if __name__ == '__main__':
    app.run(debug=True)
