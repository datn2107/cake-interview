import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from dependencies.middlewares import LoggerMiddleware
from dependencies.logger import MyLogger
from routers import user

app = FastAPI()

app.add_middleware(LoggerMiddleware, logger=MyLogger(os.path.basename(os.path.dirname(__file__))))

app.include_router(user.router)
