# app/main.py

from fastapi import FastAPI
from .routes import auth, home, stocks

app = FastAPI()

# Register the routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(home.router, prefix="/home", tags=["Home"])
app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
