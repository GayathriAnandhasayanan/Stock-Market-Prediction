# app/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db_connection, get_hashed_password_from_db
from app.models import User
from app.utils.authentication import get_password_hash

router = APIRouter()


@router.post("/register/")
def register(username: str, password: str, db=Depends(get_db_connection)):
    # Check if the user already exists
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
    user_exists = cursor.fetchone()

    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user instance
    user = User(username=username, password=get_password_hash(password))

    # Save the user to PostgreSQL
    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (user.username, user.password)
    cursor.execute(insert_query, values)

    db.commit()
    cursor.close()

    return {"message": "User registered successfully"}


@router.post("/login/")
def login(username: str, password: str):
    hashed_password_from_db = get_hashed_password_from_db(username)
    if hashed_password_from_db == get_password_hash(password):
        return {"message": "Login successful!"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
