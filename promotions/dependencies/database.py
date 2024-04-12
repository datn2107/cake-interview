import os
import motor.motor_asyncio


class MongoDb:
    client = None
    database = None

    @staticmethod
    def connect():
        MongoDb.client = motor.motor_asyncio.AsyncIOMotorClient(
            os.getenv("DB_URI").format(
                username=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD")
            ),
            retryWrites=True,
        )
        MongoDb.database = MongoDb.client.get_database(os.getenv("DB_NAME"))

    @staticmethod
    def disconnect():
        MongoDb.client.close()
