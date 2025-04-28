from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Part(Base):
    """
    Part model representing a part in the database.
    """
    __tablename__ = "part"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(30), nullable=False, unique=True)
    description = Column(String(1024))
    weight_ounces = Column(Integer)
    is_active = Column(Boolean, default=True) 