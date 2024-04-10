import os

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv("DB_URI").format(
        username=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD")
    ),
    retryWrites=True,
)

database = client.get_database(os.getenv("DB_NAME"))
