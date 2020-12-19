import datetime
import sqlalchemy.orm as orm
from sqlalchemy import *
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..db_session import SqlAlchemyBase
from data import db_session


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    # Модель пользователя
    __tablename__ = 'users'

    # ID пользователя
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Логин
    login = Column(String, nullable=False, unique=True)
    # Отображаемое имя
    name = Column(String, nullable=False, unique=True)
    # Хэшированный пароль
    hashed_password = Column(String, nullable=False)
    # Дата регистрации (сейчас не используется)
    registration_date = Column(DateTime, default=datetime.datetime.now)
    # Токен авторизации
    token = Column(String, nullable=True)

    # Установить пароль
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Проверить пароль
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class ChatileAnonymousUser:
    # Класс анонимного пользователя с заглушками. Нужен для внутренней работы Flask-Login
    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None

    def set_password(self, password):
        return

    def check_password(self, password):
        return False