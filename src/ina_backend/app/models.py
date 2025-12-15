from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.sql import text
from .database import Base


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    client_policy_api_endpoint = Column(String(512), nullable=True)
    client_api_key = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # add other fields (name, plan, etc.) as needed
