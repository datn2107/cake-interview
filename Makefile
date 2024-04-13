run:
	@echo "Running server..."
	@cd ${app} && uvicorn main:app --reload --host localhost --port ${port} --workers ${workers}

run-consumer:
	@echo "Running consumer..."
	@cd ${app} && python3 consumer.py --tasks ${tasks}

create-migration:
	@echo "Creating migration file in ${app}/migrations..."
	@mkdir -p ${app}/migrations
	@touch ${app}/migrations/$(shell date +"%s")_${name}.py
	@echo "Migration file created."

migrate:
	@echo "Running migration..."
	@python3 ${app}/migrate.py
	@echo "Migration complete."

clear-cache:
	@echo "Clearing cache..."
	@find . -name '__pycache__' -type d -exec rm -rf {} +
	@echo "Cache cleared."
