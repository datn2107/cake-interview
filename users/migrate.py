import os
import dotenv

dotenv.load_dotenv()

from dependencies.database import database


if __name__ == '__main__':
    migrations_collection = database.get_collection('migrations')

    for migration in os.listdir('users/migrations'):
        if migration.endswith('.py') and migration != '__init__.py':
            if migrations_collection.find_one({'name': migration}):
                continue

            try:
                exec(open(f'users/migrations/{migration}').read())
            except Exception as e:
                print(f'Failed to run migration {migration}: {e}')
                continue

            migrations_collection.insert_one({'name': migration})
            print(f'Migration {migration} has been run successfully')
