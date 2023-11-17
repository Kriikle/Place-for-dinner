from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double, UniqueConstraint
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column

from config.connection import Base


class Limit(Base):
    __tablename__ = "limits_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False,unique=True)
    limit_cafes = Column(Integer, nullable=False)
    limit_hist_visit = Column(Integer, nullable=False)
