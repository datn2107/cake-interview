# Data Schema
## Migration
```json
{
    "_id": "string",
    "name": "string"
}
## User
```json
{
    "_id": "string",
    "username": "string",
    "email": "string",
    "phone": "string",
    "password": "string",
    "full_name": "string",
    "birthday": "datetime",
    "is_active": "boolean",
    "is_admin": "boolean",
    "is_first_login": "number",
}
index: (username) index
       (email) index
       (phone) index
```
## Promotion Campaign
```json
{
    "_id": "string",
    "name": "string",
    "discount": "number",
    "voucher_duration": "number",
    "remaining_vouchers": "number",
    "number_of_vouchers": "number",
    "is_available": "boolean",
    "description": "string"
}
index: (is_available, remaining_promotion) composite index
```
## Voucher
```json
{
    "_id": "string",
    "user_id": "string",
    "campaign_id": "string",
    "description": "string",
    "expired_at": "datatime",
    "discount": "number"
}
index: (user_id, campaign_id) composite index
```
