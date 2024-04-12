import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from dependencies.database import MongoDb
from dependencies.logger import logger
from dependencies.middlewares import LoggerMiddleware
from routers import user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # run as a startup event
    MongoDb.connect()

    yield

    # run as a shutdown event
    MongoDb.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggerMiddleware, logger=logger)
app.include_router(user.router)
