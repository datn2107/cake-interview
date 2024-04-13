> **Note**: I assume two services are from two different repositories, which means I can't utilize the code of the other service, so that the code may be duplicated a few parts.

# Implementation
## Installation and Run
- Install the dependencies
```bash
python3 -m pip install -r requirements.txt
```
- Run migration to create index
```bash
make migrate app=users
make migrate app=promotion
```
- Run the login service and promotion service
```bash
make run app=users port=5000 workers=4
make run app=promotion port=5001 workers=4
```
**Note**: `workers` is number of processes that will be created to handle the request parallelly.
- Run the consumer
```bash
make run-consumer tasks=4
```
**Note**: `tasks` is number of tasks that will be created to handle the message concurrently.

## File Structure
```bash
app
├── migrate.py # The entry point of the migration
├── consumer.py # The entry point of the message queue consumer
├── main.py # The entry point of the web service
├── routes # Director contain the routes (api endpoints)
│   ├── handler # Director contain the useful function to handle the request
│   │   ├── user.py
│   │   └── ...
│   ├── user.py
│   └── ...
├── models # Directory contain the data model
│   ├── user.py
│   └── ...
├── repositories # Directory contain the repository to interact with the database
│   ├── user_repository.py
│   └── ...
├── dependencies # Directory contain the dependencies that will be used throughout the app
│   ├── database.py
│   ├── logger.py
│   └── ...
├── message_queue # Directory contain the code for the message queue
│   ├── consumer # Directory contain the consumer code
│   │   ├── promotion.py
│   │   └── ...
│   ├── producer # Directory contain the producer code
│   │   ├── promotion.py
│   │   └── ...
└── logs # The log directory
```

## Migration
- The migration will create the index for the collection in MongoDB
- Each migration will has the name as the format `{timestamp}_{migration_name}.py`
- The migration will be run in the order of the timestampa and log into the migration collection in MongoDB, to ensure that the migration is run only once.

## AsyncIO
- I utilize all the power of `asyncio`, that handle multiple reqeust from single process, by using:
    - `uvicorn` as the ASGI server
    - `FastAPI` as the async web framework
    - `aio_pika` as the async RabbitMQ client
    - `motor` as the async MongoDB client

## Message Queue
Message Schema between login service and promotion service
```json
{
    "user_id": "string",
    "user_identifier": "string" // which is the field that user use to login
}
```
### Producer
- The message will send to the message queue when the user first login to the system
- The queue is `durable` and the delivery mode of message is `persistent`

### Consumer
- Consumer can handle multiple messages concurrently by `asyncio` on single process
- The `prefetch_count` of consummer is the number of messages that will be sent to the consumer at once. (it is equal to the number of `tasks` that can be run concurrently).
- If the message is processed successfully, the consumer will send the `ack` to the message queue.
- Otherwise, consumer will send the `nack` to the message queue, and the message will be requeued.

## Logging
- I use the logging library to log the message to the console and the file
- The log directory is `logs` for each app and is sperated by three type: `web`, `migration`, `message_queue`, and two level: `info`, `error`
```bash
app
├── logs
    ├── message_queue
    │   ├── error.log
    │   └── info.log
    ├── migration
    │   ├── ...
    └── web
        ├── ...
```
