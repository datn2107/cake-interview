import os
import asyncio
import traceback
from datetime import datetime, timezone, timedelta
from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage
from motor.motor_asyncio import AsyncIOMotorClientSession as AgnosticClientSession

from models import Voucher, Campaign
from repositories import VoucherRepository, CampaignRepository
from dependencies.database import MongoDb
from dependencies.logger import rabbitmq_logger as logger


def create_voucher(payload: dict, available_campaign: Campaign):
    return Voucher(
        id=None,
        user_id=payload["user_id"],
        campaign_id=available_campaign.id,
        discount=available_campaign.discount,
        expired_at=(
            datetime.now(timezone.utc)
            + timedelta(days=available_campaign.voucher_duration)
        ).strftime(os.getenv("DATETIME_FORMAT")),
        description=available_campaign.description,
    )


@MongoDb.transaction
async def add_promotion(payload: dict, session: AgnosticClientSession):
    voucher_repository = VoucherRepository(MongoDb.database)
    campaign_repository = CampaignRepository(MongoDb.database)

    available_campaign = await campaign_repository.find_available_campaign(
        session=payload["session"]
    )

    if available_campaign is not None:
        voucher = create_voucher(payload, available_campaign)

        await voucher_repository.create(voucher, session=payload["session"])
        await campaign_repository.decrease_voucher_from_campaign(
            available_campaign.id, session=payload["session"]
        )
        logger.info(f"Voucher created for user {payload['user_id']}")


async def process_message(message: AbstractIncomingMessage):
    logger.info(f"Received message: {message.body}")
    async with message.process(ignore_processed=True, requeue=True):
        sucess = False
        try:
            payload = message.body.decode()
            payload = eval(payload)

            await add_promotion(payload)
            await message.ack()

            sucess = True
            logger.info("Message processed successfully")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            logger.error(traceback.format_exc())
        finally:
            if not sucess:
                await message.nack()


async def consume_promotion_messages(loop):
    async with await connect_robust(os.getenv("MQ_URL"), loop=loop) as connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(
            os.getenv("MQ_PROMOTION_ROUTING_KEY"), durable=True, auto_delete=False
        )

        await queue.consume(add_promotion)
        await asyncio.Future()
