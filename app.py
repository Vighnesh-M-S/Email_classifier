from fastapi import FastAPI
from api import router

app = FastAPI(title="Email Classifier API")

app.include_router(router)