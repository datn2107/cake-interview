run:
	@echo "Running server..."
	@cd ${app} && uvicorn main:app --reload --host localhost --port ${port}

create-migration:
	@echo "Creating migration file in ${app}/migrations..."
	@mkdir -p ${app}/migrations
	@touch ${app}/migrations/$(shell date +"%s")_${name}.py
	@echo "Migration file created."

migrate:
	@echo "Running migration..."
	@python3 ${app}/migrate.py
	@echo "Migration complete."
