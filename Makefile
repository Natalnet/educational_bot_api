

serve:
	@uvicorn main:app --reload

dbup:
	@docker-compose up -d

dbdown:
	@docker-compose down

dbin:
	@docker exec -it mongodb bash

testing:
	@python -m pytest test