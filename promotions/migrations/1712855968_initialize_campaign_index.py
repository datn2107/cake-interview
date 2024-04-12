from dependencies.database import MongoDb

campaign_collection = MongoDb.database.get_collection("campaign")

campaign_collection.create_index({"is_available": 1, "remaining_vouchers": 1})
