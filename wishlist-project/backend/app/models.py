from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class WishItem(Base):
    __tablename__ = "wish_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(String(50))
    link = Column(String(200))
    is_achieved = Column(Boolean, default=False)

class WishItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: Optional[str] = None
    link: Optional[str] = None
    is_achieved: bool = False

class WishItemResponse(WishItemCreate):
    id: int
    
    class Config:
        from_attributes = True