#producer service
## what does service do?
first step of feature pipeline. this microservice:

- reads events from kraken ws api
- saves into kafka topic

## how to run service

## setup:
to setup random, or run service locally, you need to start the message bus (ex: redpanda) locally.
```
$ cd ../../docker-compose && make start-redpanda
```

## without using docker
 - create an '.env' file with the KAFKA_BROKER_ADDRESS
 ```
 $ cp .sample.env .env
 $ add the info and save it
 ```
 - poetry run python src/main.py


## using docker
build docker image for service, and run container
```
$ make run
```