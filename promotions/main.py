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
from message_queue.consumers.promotion import handle_promotion_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    # run as a startup event
    MongoDb.connect()
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(handle_promotion_message(loop))
    # await task
    yield
    # run as a shutdown event
    # loop.close()
    MongoDb.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggerMiddleware, logger=logger)

app.include_router(voucher.router)
app.include_router(campaign.router)
