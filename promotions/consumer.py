import argparse
import asyncio
import dotenv

dotenv.load_dotenv()

from dependencies.database import MongoDb
from message_queue.consumers.promotion import consume_promotion_messages


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", type=int, default=1, help="Number of tasks will handle concurrently")
    num_tasks = parser.parse_args().tasks

    try:
        MongoDb.connect()

        loop = asyncio.get_event_loop()
        for _ in range(num_tasks):
            loop.create_task(consume_promotion_messages(loop, num_tasks))
        loop.run_forever()
    finally:
        MongoDb.disconnect()
