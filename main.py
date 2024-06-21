from fastapi import FastAPI
from routers.users import router as user_router
from typing import Union


app = FastAPI()
app.include_router(user_router, prefix="/users")
