from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double
from sqlalchemy.orm import relationship, validates

from config.connection import Base


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    img_path = Column(String, nullable=True)
    address = Column(String, nullable=True)
    lat = Column(Double, nullable=True)
    lot = Column(Double, nullable=True)

