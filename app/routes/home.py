# app/routes/home.py

from fastapi import APIRouter, HTTPException, Depends

from app.database import get_db_connection

router = APIRouter()
