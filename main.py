from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

api = FastAPI()


@api.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@api.get("/products/", response_model=List[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@api.get("/products/{product_id}", response_model=schemas.Product)
def read_product(prduct_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, prduct_id)
    if not product:
        raise HTTPException(status_code=404, detail="item not found")
    return product


@api.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, product)


@api.delete("/products/{product_id}")
@api.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="item not found")
    crud.delete_product(db, product_id)
    return {"message": "item was deleted"}



@api.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/orders/", response_model=List[schemas.Order])
def read_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@api.patch("/orders/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_order_status(db, order_id, status)