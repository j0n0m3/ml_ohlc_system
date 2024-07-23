build:
	docker build -t	trade_producer .

run: build
		docker run \
			--network=redpanda_network \
			--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
			--env-file .env
			kafka_to_feature_store

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format .

line-and-format: lint format