# Requirements
1. The login/create system:
    - User can create an account
    - User can login to their account
2. The promotion system:
    - The 100 first login users will get a 30% discount
    - This discount will be applied to the 

# Assumptions
1. For the login/create system:
    - Because the system serve for the bank so one user only have one account.
    - Because the system serve for the bank so the login session/token will be expired after 30 minutes, for the security reason. After that, user has to login again.
    - Because I only care about the backend, I will assume that the data send to server has beed encrypted and sent securely by TLS or the similar protocol.
2. For the promotion system:
    - There is only one campaign at a time. Because if it multiple campagain we could handle it by increasing number of users will get discount.

# Solution
* Authentication method: **JWT Token**
    - I use the token-based authentication, which will reduce the load on the server and make the system easier to scale.
* Framework: **FastAPI**
    - I use FastAPI, because it is one of the fastest web frameworks for Python. It is also support asyncio, which is good for the system that need to handle many concurrent requests.
* Database: **MongoDB**
    - I use MongoDB, because the system doesn't need to have a complex relationship between the data, and it easy to scale horizontally.
## System Architecture
![System Architecture](/system_diagram.png)
- **Server**: In order to serve 100000 users, we need to have server that can be scaled horizontally. And we also need to have a load balancer to distribute the load to the servers.
- **Database**: Because the number of write operations is less than the number of read operations, so to scale database I choose to create duplicate read-only databases and use the load balancer to distribute the read operations to the databases. And also have the support of the cache system to reduce the load on the database.

# API Documentation
## Create User
- **URL**: `/users`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
- **Response**:
    ```json
    {
        "username": "string",
        "id": "string"
    }
    ```
## Login
- **URL**: `/login`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
- **Response**:
    ```json
    {
        "token": "string"
    }
    ```
## Get User
- **URL**: `/users/{user_id}`
- **Method**: `GET`
- **Request Header**:
    - `Authorization`: `Bearer {token}`
- **Response**:
    ```json
    {
        "username": "string",
        "id": "string"
    }
    ```
## Get Promotion
- **URL**: `/promotion`
- **Method**: `GET`
- **Request Header**:
    - `Authorization`: `Bearer {token}`
- **Response**:
    ```json
    {
        "name": "string",
        "discount": "number",
        "description": "string"
    }
    ```
