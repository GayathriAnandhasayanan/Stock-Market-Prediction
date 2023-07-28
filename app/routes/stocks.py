# app/routes/stocks.py

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import List

from app.database import get_db_connection, get_all_predictions
from app.models import PredictionData

router = APIRouter()

# @router.post("/favorite/{stock_id}/", response_model=schemas.Stock)
# def mark_favorite(stock_id: int, db = Depends(get_db_connection)):
#     stock = crud.get_stock(db, stock_id)
#     if stock is None:
#         raise HTTPException(status_code=404, detail="Stock not found")
#     stock.is_favorite = not stock.is_favorite
#     db.commit()
#     db.refresh(stock)
#     return stock


@router.get("/predictions/")
def get_predictions_route():
    predictions = get_all_predictions()
    return {"predictions": predictions}


@router.post("/insert_data/", response_model=dict)
async def insert_data(request: Request, db=Depends(get_db_connection)):
    try:
        prediction_data = await request.json()
        cursor = db.cursor()

        for prediction in prediction_data:
            sql_query = """
            INSERT INTO predictions (stock_code, prediction_date, predicted_value, predicted_date)
            VALUES (%s, %s, %s, %s)
            """
            data = PredictionData(stock_code=prediction['stock_code'],
                                  prediction_date=prediction['prediction_date'],
                                  predicted_value=prediction['predicted_value'],
                                  predicted_date=prediction['predicted_date'])
            values = (data.stock_code, data.prediction_date, data.predicted_value, data.predicted_date)
            cursor.execute(sql_query, values)

        db.commit()
        cursor.close()
        return {"message": "Data inserted successfully"}
    except Exception as e:
        print(Exception)
        return {"message": "Task Failed successfully"}