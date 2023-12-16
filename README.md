# Vendor-Management-System
A Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.


#### You can use Swagger for ease of using the APIs.


## API Reference


### Get Token
<br/>

```http
  GET /api-token-auth/
```
#### Pass the token in the headers to get authenticated. (Format - token 'your-token')

<br/>

### Vendor
<br/>

#### Get vendors list

```http
  GET /api/vendors/
```
  | Type     | Description                       |
 | :------- | :-------------------------------- |
|     `json`          | Get the vendor data response. |

#### Create vendor

```http
  POST /api/vendors/
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `{            | `json` | **Required**. name, contact_details, address, vendor_code |
  **"name"**: "name",
  **"contact_details"**: "contact_details",
  **"address"**: "address",
  **"vendor_code"**: "vendor_code",
  **"on_time_delivery_rate"**: "on_time_delivery_rate",
  **"quality_rating_avg"**: "quality_rating_avg",
  **"average_response_time"**: "average_response_time",
  **"fulfillment_rate"**: "fulfillment_rate"
}`



#### Get specific vendor
```http
  GET /api/vendors/{vendor_id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| id          | `int` | Get the specific vendor data response. |


#### Get specific vendor
```http
  GET /api/vendors/{vendor_id}/performance
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| id          | `int` | Get the specific vendor performance data response. |
  


#### Update Vendor
```http
  PUT /api/vendors/{vendor_id}/
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `{            | `json` | **Required**. id
  **"name"**: "name",
  **"contact_details"**: "contact_details",
  **"address"**: "address",
  **"vendor_code"**: "vendor_code",
  **"on_time_delivery_rate"**: "on_time_delivery_rate",
  **"quality_rating_avg"**: "quality_rating_avg",
  **"average_response_time"**: "average_response_time",
  **"fulfillment_rate"**: "fulfillment_rate"
}`




#### Delete Vendor
```http
  DELETE /api/vendors/{vendor_id}/
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| id          | `int` | Delete the specific vendor. |

<br>
<br>


### Purchase Order
<br/>

#### Get purchase order list

```http
  GET /api/purchase_orders/
```
  | Type     | Description                       |
 | :------- | :-------------------------------- |
|     `json`          | Get all the purchase order data response. |

#### Create purchase order

```http
  POST /api/purchase_orders/
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `{            | `json` | **Required**. all
  **"po_number"**: "po_number",
  **"order_date"**: "order_date",
  **"delivery_date"**: "delivery_date",
  **"items"**: "{ json data }",
  **"quantity"**: "quantity",
  **"status"**: "status",
  **"quality_rating"**: "quality_rating",
  **"issue_date"**: "issue_date",
  **"acknowledgment_date"**: "acknowledgment_date",
  **"vendor"**: "vendor_id"
}`



#### Get specific purchase order
```http
  GET /api/purchase_orders/{po_id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| id          | `int` | Get the specific purchase order's data response. |
  


#### Update Purchase Order
```http
  PUT /api/purchase_orders/{po_id}/
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `{            | `json` | **Required**. id
  **"po_number"**: "po_number",
  **"order_date"**: "order_date",
  **"delivery_date"**: "delivery_date",
  **"items"**: "{ json data }",
  **"quantity"**: "quantity",
  **"status"**: "status",
  **"quality_rating"**: "quality_rating",
  **"issue_date"**: "issue_date",
  **"acknowledgment_date"**: "acknowledgment_date",
  **"vendor"**: "vendor_id"
}`




#### Delete Purchase Order
```http
  DELETE /api/purchase_orders/{po_id}/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| id          | `int` | Delete the specific vendor. |

<br/>
<br/>

### Historical Performance

```http
  GET /api/historical_performance/
```
  | Type     | Description                       |
 | :------- | :-------------------------------- |
|     `json`          | Get the historical_performance of vendor. |


## Installation

#### Install Vendor-Management-System with git:

```bash
  https://github.com/ugauniyal/Vendor-Management-System.git
  cd Vendor-Management-System/vendorapp
```

#### Run Vendor-Management-System:

```bash
  python manage.py runserver
```

<br>

## Screenshots

### Purchase Orders and Historical Performance
![Purchase Orders and Historical Performance Screenshot](https://cdn.discordapp.com/attachments/438420692007125031/1183490818972078160/Screenshot_from_2023-12-11_00-59-12.png?ex=658886b7&is=657611b7&hm=dd9b2af97f3d442ef9b5661c1f37628e429e87eabb32d116d76a21918d7333c7&)

<br>

### Vendors
![Vendors Screenshot](https://cdn.discordapp.com/attachments/438420692007125031/1183490819253092463/Screenshot_from_2023-12-11_00-59-42.png?ex=658886b7&is=657611b7&hm=80656024aac3eee4c756735e68b4f5e4b0f867fa26fe65f4efb7963b8bfdd98c&)


## Running Tests

To run tests, run the following command.

```bash
  python manage.py vendorapp.test
```


## Running Celery Tasks

Firstly run redis (broker).

```bash
  redis-server
```



To run celery tasks, run the following command.


Celery Worker

```bash
  celery -A mysite worker -l info
```

<br/>

Celery Beat for automatic scheduler

```bash
  celery -A mysite beat -l info
```
