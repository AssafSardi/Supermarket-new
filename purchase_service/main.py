import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import pandas as pd
from uuid import UUID

from fastapi import FastAPI, Depends, Request, Form, APIRouter
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

import database
import models


# Lifespan setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    database.Base.metadata.create_all(bind=database.engine)
    load_csv_data()
    yield

app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/api/v1/customer")

templates = Jinja2Templates(directory="templates")


# Utility functions
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_csv_data():
    db = database.SessionLocal()
    try:
        # Load products to DB
        products_path = os.path.join(os.getcwd(), "data", "products_list.csv")
        if os.path.exists(products_path):
            df_products = pd.read_csv(products_path)
            for _, row in df_products.iterrows():
                try:
                    db.execute(
                        text("INSERT INTO products (product_name, unit_price) VALUES (:name, :price)"),
                        {"name": row["product_name"], "price": row["unit_price"]}
                    )
                except IntegrityError:
                    db.rollback()
                else:
                    db.commit()

        # Load purchases history to DB
        purchases_path = os.path.join(os.getcwd(), "data", "purchases.csv")
        if os.path.exists(purchases_path):
            df_purchases = pd.read_csv(purchases_path)
            for _, row in df_purchases.iterrows():
                try:
                    db.execute(
                        text("""
                        INSERT INTO purchases (supermarket_id, timestamp, user_id, items_list, total_amount)
                        VALUES (:smkt_id, :ts, :uid, :items, :total)
                        """),
                        {
                            "smkt_id": row["supermarket_id"],
                            "ts": row["timestamp"],
                            "uid": row["user_id"],
                            "items": row["items_list"],
                            "total": row["total_amount"]
                        }
                    )
                except IntegrityError:
                    db.rollback()
                else:
                    db.commit()
    finally:
        db.close()


@router.get("/purchase", response_class=HTMLResponse)
def purchase_form(request: Request, db: Session = Depends(get_db)):
    user_ids = db.execute(text("SELECT DISTINCT user_id FROM purchases ORDER BY user_id ASC")).fetchall()
    products = db.execute(text("SELECT product_name, unit_price FROM products")).fetchall()
    return templates.TemplateResponse("purchase.html", {
        "request": request,
        "users": [str(user)[7:-4] for user in user_ids],
        "supermarkets": ["SMKT001", "SMKT002", "SMKT003"],
        "products": [(row[0], row[1]) for row in products]
    })


@router.post("/purchase")
def purchase(supermarket_id: str = Form(...), existing: str=Form("no"), user_id: Optional[str]=Form(None), items: list[str]=Form(...), db: Session = Depends(get_db)):
    # Validate a supermarket branch was selected
    if not supermarket_id:
        return {"error": "supermarket must be selected for purchase"}

    # Validate user_id
    if existing == "yes":
        if not user_id:
            return {"error": "user_id is required for existing users"}
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return {"error": "user_id is not a valid UUID"}

        # Verify user_id exists in DB
        exists = db.execute(
            text("SELECT 1 FROM purchases WHERE user_id = :user_id"),
            {"user_id": str(user_uuid)}
        ).first()

        if not exists:
            return {"error": "user_id does not exist"}
    else:
        user_uuid = uuid.uuid4()

    # Get products data for those in items_list and calculate the total amount
    products_rows = db.execute(
        text("SELECT product_name, unit_price FROM products WHERE product_name = ANY(:items)"),
        {"items": items}
    ).fetchall()

    product_prices = {row[0]: float(row[1]) for row in products_rows}
    total_amount = sum(product_prices.values())

    # Store new Purchase record to DB
    purchase = models.Purchase(
        supermarket_id=supermarket_id,
        timestamp=datetime.now(),
        user_id=user_uuid,
        items_list=','.join(item.strip() for item in items),
        total_amount=total_amount
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return purchase


@router.get("/supermarkets")
def get_supermarkets():
    return {"Supermarkets": ["SMKT001", "SMKT002", "SMKT003"]}


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.execute(text("SELECT product_name, unit_price FROM products")).fetchall()

    return {"Products": [{"product_name": row[0], "unit_price": float(row[1])} for row in products]}


app.include_router(router)