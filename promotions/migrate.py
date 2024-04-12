import os
import dotenv

dotenv.load_dotenv()

from dependencies.logger import migrations_logger as logger
from dependencies.database import MongoDb


if __name__ == '__main__':
    try:
        MongoDb.connect()
        migrations_collection = MongoDb.database.get_collection('migrations')

        for migration in os.listdir('users/migrations'):
            if not migration.endswith('.py') or migration == '__init__.py':
                continue

            if migrations_collection.find_one({'name': migration}):
                continue

            try:
                exec(open(f'users/migrations/{migration}').read())
            except Exception as e:
                logger.error(f'Failed to run migration {migration}: {e}')
                continue

            migrations_collection.insert_one({'name': migration})
            logger.info(f'Migration {migration} has been run successfully')
    finally:
        MongoDb.disconnect()
