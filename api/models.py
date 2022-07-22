from datetime import datetime, timedelta
import sqlalchemy as sqla
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm as orm
from werkzeug.security import generate_password_hash, check_password_hash
from api.app import db


class Updatable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class User(Updatable, db.Model):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    password = Column(String(128))
    registrationDate = Column(DateTime, default=datetime.utcnow)
    role = Column(Integer, ForeignKey('UserRole.id'))


class UserRole(db.Model):
    __tablename__ = 'UserRole'

    id = Column(Integer, primary_key=True)
    roleName = Column(String(64), unique=True, nullable=False)
    roleDescription = Column(String(128))

    user = relationship('User', back_populates='users')
    userRoleRights = relationship('UserRoleRights', back_populates='rights')

    def get_rights(self):
        return [i.right for i in self.rights]


class UserRoleRights(db.Model):
    __tablename__ = 'UserRoleRights'

    id = Column(Integer, primary_key=True)
    role = Column(Integer, ForeignKey('UserRole.id', ondelete='CASCADE'))
    right = Column(String(64), nullable=False)



