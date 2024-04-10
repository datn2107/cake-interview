import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from routers import user

app = FastAPI()
app.include_router(user.router)
