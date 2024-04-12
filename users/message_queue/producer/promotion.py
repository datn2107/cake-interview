import os
import aio_pika
from aio_pika import connect_robust, Message, DeliveryMode


async def push_promotion_message(payload: dict, routing_key: str) -> None:
    async with connect_robust(os.getenv("MQ_URL")) as connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            Message(body=str(payload).encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=routing_key,
        )
