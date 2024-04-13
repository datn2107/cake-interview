import os
import dotenv
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

dotenv.load_dotenv()

from dependencies.logger import migrations_logger as logger
from dependencies.database import MongoDb


def run_migration(migration: str, migrations_collection: AsyncIOMotorClient):
    try:
        exec(open(f"{migration_dir}/{migration}").read())
    except Exception as e:
        logger.error(f"Failed to run migration {migration}: {e}")
        return

    migrations_collection.insert_one({"name": migration})
    logger.info(f"Migration {migration} has been run successfully")


if __name__ == "__main__":
    try:
        MongoDb.connect()
        loop = asyncio.get_event_loop()
        migrations_collection = MongoDb.database.get_collection("migrations")

        app_name = os.path.basename(os.path.dirname(__file__))
        migration_dir = os.path.join(app_name, "migrations")

        migrations = os.listdir(migration_dir)
        migrations.sort()
        for migration in migrations:
            if not migration.endswith(".py") or migration == "__init__.py":
                continue

            migration_in_db = loop.run_until_complete(
                migrations_collection.find_one({"name": migration})
            )
            if migration_in_db is not None:
                continue

            run_migration(migration, migrations_collection)
    finally:
        MongoDb.disconnect()
