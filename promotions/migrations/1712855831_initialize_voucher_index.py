from dependencies.database import MongoDb

voucher_collection = MongoDb.database.get_collection("voucher")

voucher_collection.create_index({"user_id": 1, "expired_at": 1})
