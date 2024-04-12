import asyncio
import dotenv

dotenv.load_dotenv()

from dependencies.database import MongoDb
from message_queue.consumers.promotion import consume_promotion_messages


if __name__ == "__main__":
    try:
        MongoDb.connect()

        loop = asyncio.get_event_loop()
        loop.create_task(consume_promotion_messages(loop))
        loop.run_forever()
    finally:
        MongoDb.disconnect()
