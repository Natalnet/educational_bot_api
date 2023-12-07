

serve api:
	@uvicorn api.main:app --reload

db up:
	@docker-compose up -d

db down:
	@docker-compose down

db in:
	@docker exec -it mongodb bash

testing:
	@python -m pytest test