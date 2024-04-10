from dependencies.database import database

users_collection = database.get_collection("users")

users_collection.create_index("username")
users_collection.create_index("email")
users_collection.create_index("phone")
