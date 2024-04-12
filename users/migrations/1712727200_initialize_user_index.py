from dependencies.database import MongoDb

users_collection = MongoDb.database.get_collection("users")

users_collection.create_index("username")
users_collection.create_index("email")
users_collection.create_index("phone")
