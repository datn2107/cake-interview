# API Documentation

# Work Flow
## User create an account
![Register](docs/images/user_register.png)

## User login to their account
![Login](docs/images/user_login.png)

## Create a promotion campaign
![Promotion](docs/images/create_campaign.png)

## Promotion service handle the first login user
![Promotion](docs/images/create_voucher.png)

## User get the promotion
![Promotion](docs/images/get_promotion.png)

# API Documentation
1. **Register**
    - **URL**: `/register`
    - **Method**: `POST`
    - **Request Body**:
    ```json
    {
        "username": "string",
        "email": "string",
        "phone": "string",
        "password": "string",
        "full_name": "string",
        "birthday": "datetime"
    }
    ```
    - **Response**:
    ```json
    { // 200 OK
        "status": "success",
    }
    { // 400 Bad Request
        "status": "error",
        "message": "error message"
    }
    ```
2. **Login**
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
    { // 200 OK
        "status": "success",
        "token": "string"
    }
    { // 400 Bad Request
        "status": "error",
        "message": "error message"
    }
    ```
3. **Get Vounchers**
    - **URL**: `/vouchers`
    - **Method**: `GET`
    - **Request Header**:
    ```json
    {
        "Authorization": "Bearer <token>"
    }
    ```
    - **Response**:
    ```json
    { // 200 OK
        "status": "success",
        "vouchers": [
            {
                "id": "string",
                "user_id": "string",
                "campaign_id": "string",
                "description": "string",
                "expired_at": "datatime",
                "discount": "number"
            }
        ]
    }
    { // 400 Bad Request
        "status": "error",
        "message": "error message"
    }
    ```
4. **Redeem Voucher**
    - **URL**: `/vouchers/redeem`
    - **Method**: `POST`
    - **Request Header**:
    ```json
    {
        "Authorization": "Bearer <token>"
    }
    ```
    - **Request Body**:
    ```json
    { // 200 OK
        "status": "success",
        "message": "Voucher redeemed"
    }
    { // 400 Bad Request
        "status": "error",
        "message": "error message"
    }
    ```
5. **Create Campaign**
    - **URL**: `/campaigns`
    - **Method**: `POST`
    - **Request Header**:
    ```json
    {
        "Authorization": "Bearer <token>"
    }
    ```
    - **Request Body**:
    ```json
    {
        "name": "string",
        "discount": "number",
        "number_of_vouchers": "number",
        "description": "string"
    }
    ```
