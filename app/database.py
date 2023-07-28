# database.py

import psycopg2
from fastapi import HTTPException

# Replace these values with your actual PostgreSQL database credentials
DB_NAME = "neondb"
DB_USER = "ahmobayen"
DB_PASSWORD = "85hSGYVTLHZf"
DB_HOST = "ep-green-salad-117547.eu-central-1.aws.neon.tech"
DB_PORT = "5432"


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def get_hashed_password_from_db(username: str):
    # Replace these with your actual database credentials

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Execute a SELECT query to retrieve the hashed_password for the given username
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            # The query returned a result, so we found the user in the database
            hashed_password_from_db = result[0]
            return hashed_password_from_db

        # The query did not return a result, which means the username doesn't exist in the database
        return None

    except Exception as e:
        # Handle any errors that might occur during the database connection or query
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        # Close the database connection and cursor when done
        cursor.close()
        connection.close()


def get_all_predictions():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT stock_code, prediction_date, predicted_value, predicted_date FROM predictions;"
    cursor.execute(query)
    predictions = cursor.fetchall()
    cursor.close()
    return predictions
