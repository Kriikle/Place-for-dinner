from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship, validates

from config.connection import Base
from core.models.restaurant import Restaurant
from core.models.user import User


class Dinner(Base):
    __tablename__ = "dinner"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    restaurant = relationship(Restaurant, foreign_keys=[restaurant_id], back_populates="dinner")
    user = relationship(User, foreign_keys=[user_id], back_populates="dinner")
