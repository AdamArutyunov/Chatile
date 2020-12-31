import datetime
import sqlalchemy.orm as orm
from sqlalchemy import *
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..db_session import SqlAlchemyBase
from data import db_session


class Message(SqlAlchemyBase, SerializerMixin):
    # Модель сообщения
    __tablename__ = 'messages'

    # ID сообщения
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Данные сообщения
    data = Column(String, nullable=False)

    # Отправитель
    sender_login = Column(String, ForeignKey("users.login"))
    sender = orm.relation("User", foreign_keys=[sender_login])

    # Получатель
    recipient_login = Column(String, ForeignKey("users.login"))
    recipient = orm.relation("User", foreign_keys=[recipient_login])

    # Дата отправки
    sending_date = Column(DateTime, default=datetime.datetime.now)
