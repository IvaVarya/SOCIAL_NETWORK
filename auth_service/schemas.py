#schemas.py
from marshmallow import Schema, fields, validate, ValidationError
import re

class UserSchema(Schema):
    first_name = fields.Str(required=True, validate=[
        validate.Length(min=1, max=50),
        validate.Regexp(r'^[A-ZА-Я][a-zа-я]*$', error="Имя должно начинаться с заглавной буквы и содержать только буквы.")
    ])
    last_name = fields.Str(required=True, validate=[
        validate.Length(min=1, max=50),
        validate.Regexp(r'^[A-ZА-Я][a-zа-я]*$', error="Фамилия должна начинаться с заглавной буквы и содержать только буквы.")
    ])
    login = fields.Str(required=True, validate=[
        validate.Length(min=3, max=20),
        validate.Regexp(r'^[a-zA-Z0-9_]+$', error="Логин должен содержать только латинские буквы, цифры и символ подчеркивания.")
    ])
    password = fields.Str(required=True, validate=[
        validate.Length(min=6),
        validate.Regexp(r'^(?=.*[A-Za-z])(?=.*\d).{6,}$', 
                       error="Пароль должен содержать минимум 6 символов, включая хотя бы одну букву и одну цифру.")
    ])
    confirm_password = fields.Str(required=True)
    mail = fields.Email(required=True)

    def validate(self, data, **kwargs):
        # Проверка наличия confirm_password в данных
        if 'confirm_password' not in data:
            raise ValidationError("Поле 'confirm_password' обязательно.", field_name="confirm_password")
        
        # Проверка совпадения пароля и подтверждения пароля
        if data['password'] != data['confirm_password']:
            raise ValidationError("Пароли не совпадают.", field_name="confirm_password")
        
        return super().validate(data, **kwargs)