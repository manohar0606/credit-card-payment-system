from fastapi import FastAPI
from fast_api.routes.payment import router as payment_router

app = FastAPI()

app.include_router(payment_router)


@app.get("/")
def home():
    return {
        "message": "FastAPI Payment System is running"
    }