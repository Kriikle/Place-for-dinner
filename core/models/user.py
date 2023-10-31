from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.connection import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=True, )

    restaurants = relationship("Restaurant", cascade='all, delete', lazy='dynamic', back_populates="user")
    dinner = relationship("Dinner", cascade='all, delete', lazy='dynamic', back_populates="user")

    def __repr__(self):
        return '{} {} {}'.format(self.lastname, self.firstname, self.patronymic)
