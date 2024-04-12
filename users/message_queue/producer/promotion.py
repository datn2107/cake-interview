import os
import aio_pika
from aio_pika import connect_robust, Message, DeliveryMode

from dependencies.logger import web_logger as logger


async def push_promotion_message(payload: dict, routing_key: str) -> None:
    connection = connect_robust(os.getenv("MQ_URL"))

    async with connection:
        channel = await connection.channel()

        logger.info(f"Publishing message: {payload}")
        await channel.default_exchange.publish(
            Message(body=str(payload).encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=routing_key,
        )
