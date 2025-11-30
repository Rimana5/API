from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, database
from .database import get_db

app = FastAPI(title="Wishlist API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Wishlist API is running!"}

# Все эндпоинты с префиксом /api
@app.post("/api/wishlist/", response_model=models.WishItemResponse)
def create_wish_item(item: models.WishItemCreate, db: Session = Depends(get_db)):
    db_item = models.WishItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/api/wishlist/", response_model=List[models.WishItemResponse])
def read_wish_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.WishItem).offset(skip).limit(limit).all()
    return items

@app.get("/api/wishlist/{item_id}", response_model=models.WishItemResponse)
def read_wish_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.WishItem).filter(models.WishItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/api/wishlist/{item_id}", response_model=models.WishItemResponse)
def update_wish_item(item_id: int, item_update: models.WishItemCreate, db: Session = Depends(get_db)):
    item = db.query(models.WishItem).filter(models.WishItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item_update.dict().items():
        setattr(item, key, value)
    
    db.commit()
    db.refresh(item)
    return item

@app.delete("/api/wishlist/{item_id}")
def delete_wish_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.WishItem).filter(models.WishItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}