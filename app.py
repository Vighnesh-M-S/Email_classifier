from fastapi import FastAPI
from api import router

app = FastAPI(title="Email Classification API")
app.include_router(router)