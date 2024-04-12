import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from dependencies.logger import logger
from dependencies.middlewares import LoggerMiddleware
from routers import user


app = FastAPI()
app.add_middleware(LoggerMiddleware, logger=logger)
app.include_router(user.router)
