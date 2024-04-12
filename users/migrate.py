import os
import dotenv

dotenv.load_dotenv()

from dependencies.logger import MyLogger
from dependencies.database import MongoDb


if __name__ == '__main__':
    logger = MyLogger(os.path.basename(os.path.dirname(__file__)) + ":migrate")

    try:
        MongoDb.connect()
        migrations_collection = MongoDb.database.get_collection('migrations')

        for migration in os.listdir('users/migrations'):
            if migration.endswith('.py') and migration != '__init__.py':
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
