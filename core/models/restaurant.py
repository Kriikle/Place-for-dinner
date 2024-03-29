from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double, UniqueConstraint
from sqlalchemy.orm import relationship, validates

from config.connection import Base
from core.models.user import User


class Restaurant(Base):
    __tablename__ = "restaurant"
    __table_args__ = (
        UniqueConstraint('user_id', 'name'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)
    img_path = Column(String, nullable=True)
    address = Column(String, nullable=True)
    lat = Column(Double, nullable=True)
    lot = Column(Double, nullable=True)

    user = relationship(User, foreign_keys=[user_id], back_populates="restaurants")
    dinner = relationship("Dinner", cascade='all, delete', lazy='dynamic', back_populates="restaurant")
