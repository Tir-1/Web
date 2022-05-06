import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Tags_of_map(SqlAlchemyBase):
    __tablename__ = 'tags'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    color = sqlalchemy.Column(sqlalchemy.String, default="pmwtm", nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coord = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    in_directory = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship("User", backref='tags')
