import os
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

from dependencies.database import MongoDb
from dependencies.middlewares import LoggerMiddleware
from dependencies.logger import web_logger as logger
from routers import voucher, campaign


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

app.include_router(voucher.router)
app.include_router(campaign.router)
