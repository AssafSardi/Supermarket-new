from fastapi import FastAPI, Depends, APIRouter, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

import database

app = FastAPI()
router = APIRouter(prefix="/api/v1/owner")

templates = Jinja2Templates(directory="templates")

# Utility functions
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard", response_class=HTMLResponse)
def owner_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/unique-customers")
def unique_customers(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT COUNT(DISTINCT user_id) FROM purchases
    """)).scalar()

    return {"unique_customers" : result}


@router.get("/loyal-customers")
def loyal_customers(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT user_id, COUNT(*) AS times FROM purchases
        GROUP BY user_id
        HAVING COUNT(*) >= 3
    """)).fetchall()

    return {"loyal_customers" : {"total": len(result), "customers": [{"user_id": str(row[0]), "times_purchased": row[1]} for row in result]}}


@router.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    result = db.execute(text("""
        WITH ranked_items AS (
            SELECT
                item,
                COUNT(*) AS times_purchased,
                DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
            FROM (
                SELECT UNNEST(STRING_TO_ARRAY(items_list, ',')) AS item
                FROM purchases
            ) AS all_items
            GROUP BY item
        )
        SELECT item, times_purchased
        FROM ranked_items
        WHERE rank <= 3
        ORDER BY times_purchased DESC
    """)).fetchall()

    return {"top_products" : [{"product_name": row[0], "times_was_purchased": row[1]} for row in result]}


app.include_router(router)