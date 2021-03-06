import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Directory(SqlAlchemyBase):  # Класс хранящий информацию об альбомах пользователя
    __tablename__ = 'directories'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship("User", backref='directories')
