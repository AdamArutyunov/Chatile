import datetime
import jwt
import bcrypt
import sqlalchemy.orm as orm
from sqlalchemy import *
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..db_session import SqlAlchemyBase
from lib.Packets import *
from data import db_session
from Constants import *


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    # Модель пользователя
    __tablename__ = 'users'

    # Логин
    login = Column(String, nullable=False, primary_key=True)
    # Отображаемое имя
    name = Column(String, nullable=False)
    # Хэшированный пароль
    hashed_password = Column(String, nullable=False)
    # Дата регистрации (сейчас не используется)
    registration_date = Column(DateTime, default=datetime.datetime.now)
    # Токен авторизации
    token = Column(String, nullable=True)
    # Дата последнего онлайна
    last_online_date = Column(DateTime, default=datetime.datetime.now)

    # Установить пароль
    def set_password(self, password):
        self.hashed_password = password

    # Проверить пароль
    def check_password(self, password):
        return bcrypt.checkpw(password.encode(encoding='utf-8'),
                              self.hashed_password.encode(encoding='utf-8'))

    def check_auth(self, password):
        if self.check_password(password):
            self.auth()
            return AuthPacket(self.token)
        return BadLoginErrorPacket("Bad login: invalid password")

    def check_token(self, token):
        if not token:
            return False

        try:
            token = token.encode('utf-8')
            data = jwt.decode(token, SECRET_WORD)
        except jwt.ExpiredSignatureError:
            return False

        if data and "user_login" in data and data["user_login"] == self.login:
            return True

        return False

    def auth(self):
        token = jwt.encode({"user_login": self.login,
                            "exp": datetime.datetime.now() + datetime.timedelta(hours=1)}, SECRET_WORD)
        self.token = token.decode('utf-8')
        self.online()

        return AuthPacket(self.token)

    def online(self):
        self.last_online_date = datetime.datetime.now()
