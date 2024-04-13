import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from dependencies.database import MongoDb
from dependencies.logger import web_logger as logger
from dependencies.middlewares import LoggerMiddleware
from routers import user


async def startup_event():
    MongoDb.connect()


async def shutdown_event():
    MongoDb.disconnect()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event()
    yield
    await shutdown_event()


app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggerMiddleware, logger=logger)
app.include_router(user.router)
