from fastapi import FastAPI
from routers.user import router as user_router
from database import engine, Base
import models

app = FastAPI()
app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "Meeting Room Booking API"
    }


@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as connection:
            return {
                "message": "MYSQL CONNECTION OK"
            }
    except Exception as e:
        return {
            "message": "MYSQL CONNECTION ERROR",
            "error": str(e)
        }


@app.post("/create-tables")
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        return {
            "message": "TABLES CREATED SUCCESSFULLY"
        }
    except Exception as e:
        return {
            "message": "CREATE TABLES ERROR",
            "error": str(e)
        }