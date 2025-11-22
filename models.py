from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    mobile_number = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="captain")  # captain|owner|authority
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    boats = relationship("Boat", back_populates="owner")


class Boat(Base):
    __tablename__ = "boats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    registration = Column(String, unique=True, index=True, nullable=True)
    type = Column(String, nullable=True)          # e.g., fibreglass, ali, etc.
    length_m = Column(Integer, nullable=True)
    home_port = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="boats")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
