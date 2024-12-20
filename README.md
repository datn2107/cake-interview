> **Note**: I assume two services are from two different repositories, which means I can't utilize the code of the other service, so that the code may be duplicated a few parts in  `users` and `promotion` directories.

Table of Contents
=================

* [Requirements](#requirements)
* [Analysis and Assumptions](#analysis-and-assumptions)
* [Work Flow](#work-flow)
* [Solution](#solution)
    * [System Architecture](#system-architecture)
    * [Technology Stack](#technology-stack)
* [Cases Can and Can't Handle](#cases-can-and-cant-handle)

Another document:
- [Workflow, Detail Implementation and Code Structure](docs/implementation.md)
- [Data Schema](docs/data_schema.md)
- [API Documentation](docs/api_documentation.md)
- [Diagrams](https://drive.google.com/file/d/1qjLSvHa9UMELKau82q0liyZG0-yluR5_/view?usp=sharing)

# Requirements
1. The login/create system:
    - User can create an account
    - User can login to their account
2. The promotion system:
    - The 100 first login users will get a 30% discount
    - This discount will be applied to the next purchase

# Assumptions
- Because this is the service for the bank system, so I have some assumptions:
    - **One person can have only one account**, which means the username, email, and phone number must be unique.
    - **The session/token will be expired after 30 minutes**, for the security reason of the bank system. So we also **don't need to implement refresh token**.
    - Assume that the payload send to server on the sercure protocol (HTTPS).
# Insight
- **The number of read operations is much more than the number of write operations**:
    - Because each person only has one account, so the request to create new account is not too much.
    - Because each campaign will only have 100 vouchers, so the request to create new voucher is not too much.
    - But the number of login request and query the voucher of the user is very much.
- **The number of messages communicate between the login service and promotion service is not too much**:
    - Because we only need to send the message when the user first login, which is not too much.

# Work Flow
### User create an account
![Register](docs/images/user_register.png)

### User login to their account
![Login](docs/images/user_login.png)

### Promotion service handle the first login user
![Promotion](docs/images/create_voucher.png)

### Create a promotion campaign
![Promotion](docs/images/create_campaign.png)

### User get the promotion
![Promotion](docs/images/get_promotion.png)

# Solution
## System Architecture
![System Architecture](docs/images/system_diagram.png)
- **Server**
    - I choose the server that can scale horizontally, to handle multiple requests concurrently.
    - And use a load balancer to distribute the load to the servers.
- **Database**
    - I choose the database that scale horizontally by duplicating the read-only databases, because the number of read operations is much more than the number of write operations.
    - And use the load balancer to distribute the read request to the read-only databases.
    - We can also use sharding to scale the database to support if the number of users is become larger.
- **Message Queue**:
    - I use message queue (worker queue) to handle the message between the login service and promotion service.
    - Which only need one queue with multiple consumers to handle the message concurrently.
    - I choose message queue instead of direct call to avoid the delay or blocking when the user login.
- **MQ Consummer**:
    - I use the consumer that can be scaled horizontally by increase multiple servers and spawn multiple processers.
    - And utilize queue broker of RabbitMQ to be the load balancer to distribute the message to the consumers.
- **No Cache**:
    - I don't use cache in these systems, because the data is not shared too much between the users, each user has their own data, so the cache system will not be effective in this case.

## Technology Stack
* Authentication method: **JWT Token**
    - I use JWT token becasue is stateless and it doesn't need to store the token in the database, that will reduce the load of the database.
    - It also doesn't need other service send the request to login service to verify the token.
    - Read here for more detail about the [JWT Token](https://jwt.io/introduction/)
* Framework: **FastAPI**
    - Because FastAPI support `asyncio`, which can handle multiple requests concurrently in a single process.
* Server: **Uvicorn**
    - I use `Uvicorn` because it is a lightning-fast ASGI server implementation, suitable for async frameworks like FastAPI.
    - It also supports spawn multiple processes to handle the request parallelly.
* Message Queue: **RabbitMQ**
    - Becasue the number of messages is not too much, so we don't need a horizontally scalable message queue like Kafka. For simplicity, RabbitMQ has enough features to handle it.
    - I use lazy queue mode, and durable message to ensure that the message will not be lost when the server is down or out of memory.
    - For more detail about the implement of RabbitMQ, please refer to the [Implementation](docs/implementation.md) document.
* Database: **MongoDB**
    - Data of server doesn't have the relationship between the collections, so the NoSQL database is suitable for this case.
    - MongoDB can be easily scaled horizontally, by sharding the data or create the replica set.
    - It also support [Optimistic Locking](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) to handle the transaction, which guarantee the data consistency.
    - For more detail about schema, and index in each collection, please refer to the [Data Schema](docs/data_schema.md) document.
* Load Balancer:
    - My code is not implement the load balancer, I think it beeter to use the load balancer from the cloud provider, because it is more stable and has more features.
    - Just try to make my code easy to scale horizontally, so it can be easily integrated with the load balancer.

# Cases Can and Can't Handle
### Can Handle
- Data consistency when mutliple users requests to the same api at the same time. For exmaple: 2 user first login at the same time, but the number of promotion is only 1.
    + Using database transaction to ensure the data consistency.
    + Mongodb support [Optimistic Locking](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) to handle the transaction. If the (readed) data is changed by another user, the transaction will be aborted and retry
### Can't Handle
- The user first login order can't be guaranteed.
    + The message queue will ensure that the message will be processed in the order.
    + But the consumer can handle the message concurrently, so the order of the message will not be guaranteed.
- The consumer and the server can't be run in the same process.
    + Because the limitation of the current knowledge, I can't make the consumer and the server run in the same process.
- Multiple device login at the same time.
    + My code doesn't handle this, it allows multiple devices login at the same time.
