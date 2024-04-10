import os

from pymongo import mongo_client, server_api

client = mongo_client.MongoClient(
    os.getenv("DB_URI").format(
        username=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD")
    ),
    server_api=server_api.ServerApi("1"),
    retryWrites=True,
)

database = client.get_database(os.getenv("DB_NAME"))
