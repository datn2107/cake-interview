import os
import asyncio
from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage
from datetime import datetime, timezone

from models.voucher import Voucher
from dependencies.database import MongoDb
from dependencies.logger import rabbitmq_logger as logger
from repositories.campaign_repository import CampaignRepository
from repositories.voucher_repository import VoucherRepository


async def add_promotion(message: AbstractIncomingMessage):

    voucher_repository = VoucherRepository(MongoDb.database)
    campaign_repository = CampaignRepository(MongoDb.database)

    async with message.process():
        async with MongoDb.client.start_session() as session:
            async with session.start_transaction():
                payload = message.body.decode()
                logger.info(f"Received message: {payload}")

                try:
                    available_campaign = (
                        await campaign_repository.find_available_campaign(
                            payload["user_id"]
                        )
                    )

                    if available_campaign is None:
                        logger.info(
                            f"No available campaign for user {payload['user_id']}"
                        )
                    else:
                        voucher = Voucher(
                            user_id=payload["user_id"],
                            campaign_id=available_campaign.id,
                            discount=available_campaign.discount,
                            expired_at=datetime.now(timezone.utc)
                            + available_campaign.voucher_duration,
                            description=available_campaign.description,
                        )
                        await voucher_repository.create(voucher, session)

                        logger.info(f"Voucher created for user {payload['user_id']}")

                    await message.ack()
                except Exception as e:
                    logger.error(f"Error when processing message: {e}")
                    await message.nack()


async def handle_promotion_message(loop):
    connection = await connect_robust(os.getenv("MQ_URL"), loop=loop)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(
            os.getenv("MQ_PROMOTION_ROUTING_KEY"), durable=True
        )

        await queue.consume(add_promotion)
