TARGET ?= ./

lint:
	flake8 --statistics --count $(TARGET) || true

test: lint
	pytest $(TARGET)

docker-dev-up:
	docker-compose -f docker/dev/docker-compose.yml up

docker-prod-up:
	docker-compose -f docker/prod/docker-compose.yml up
