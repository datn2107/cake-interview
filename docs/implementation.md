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

## Migration
- The migration will create the index for the collection in MongoDB
- Each migration will has the name as the format `{timestamp}_{migration_name}.py`
- The migration will be run in the order of the timestampa and log into the migration collection in MongoDB, to ensure that the migration is run only once.

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
- We can config The consumer to handle multiple messages concurrently in single process, which means will interleave message when the message is I/O bound.
- Each consumer will have the `prefetch_count` equal to the number of tasks that will be created to handle the message concurrently.
- The consumer will send the `ack` to the message queue when the message is processed successfully, otherwise, the message will send the `nack` to the message queue.
- The message will be requeue if the consumer send the `nack` to the message queue.
