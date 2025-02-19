# Trading Platform API Specification

## Base URL
`https://api.tradingplatform.com/v1`

## Authentication
All API endpoints require JWT authentication token in the Authorization header:

# Trading Platform API Specification

## Base URL
`https://api.tradingplatform.com/v1`

## Authentication
All API endpoints require JWT authentication token in the Authorization header:

`Authorization: Bearer <jwt_token>`

## Endpoints

### Authentication
#### Register New User
- **POST** `/auth/register`
- **Request Body:**
  ```json
  {
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "user_id": "string",
    "token": "string"
  }
  ```

#### Login
- **POST** `/auth/login`
- **Request Body:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "token": "string",
    "user": {
      "user_id": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string"
    }
  }
  ```

### User Account
#### Get Account Overview
- **GET** `/account`
- **Response:** `200 OK`
  ```json
  {
    "account_id": "string",
    "buying_power": "number",
    "cash_balance": "number",
    "portfolio_value": "number",
    "total_return": "number",
    "total_return_percentage": "number"
  }
  ```

#### Get Account History
- **GET** `/account/history`
- **Query Parameters:**
  - `interval`: string (1D, 1W, 1M, 3M, 1Y, ALL)
- **Response:** `200 OK`
  ```json
  {
    "data_points": [
      {
        "timestamp": "string",
        "portfolio_value": "number"
      }
    ]
  }
  ```

### Stocks
#### Search Stocks
- **GET** `/stocks/search`
- **Query Parameters:**
  - `query`: string
- **Response:** `200 OK`
  ```json
  {
    "stocks": [
      {
        "symbol": "string",
        "name": "string",
        "current_price": "number",
        "price_change": "number",
        "price_change_percentage": "number"
      }
    ]
  }
  ```

#### Get Stock Details
- **GET** `/stocks/{symbol}`
- **Response:** `200 OK`
  ```json
  {
    "symbol": "string",
    "name": "string",
    "current_price": "number",
    "price_change": "number",
    "price_change_percentage": "number",
    "market_cap": "number",
    "pe_ratio": "number",
    "dividend_yield": "number",
    "about": "string",
    "news": [
      {
        "title": "string",
        "url": "string",
        "source": "string",
        "published_at": "string"
      }
    ]
  }
  ```

#### Get Stock Price History
- **GET** `/stocks/{symbol}/history`
- **Query Parameters:**
  - `interval`: string (1D, 1W, 1M, 3M, 1Y, 5Y)
- **Response:** `200 OK`
  ```json
  {
    "symbol": "string",
    "data_points": [
      {
        "timestamp": "string",
        "price": "number",
        "volume": "number"
      }
    ]
  }
  ```

### Trading
#### Place Order
- **POST** `/orders`
- **Request Body:**
  ```json
  {
    "symbol": "string",
    "type": "string (market, limit)",
    "side": "string (buy, sell)",
    "quantity": "number",
    "limit_price": "number (required for limit orders)"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "order_id": "string",
    "status": "string",
    "created_at": "string"
  }
  ```

#### Get Orders
- **GET** `/orders`
- **Query Parameters:**
  - `status`: string (open, closed)
  - `limit`: number
  - `offset`: number
- **Response:** `200 OK`
  ```json
  {
    "orders": [
      {
        "order_id": "string",
        "symbol": "string",
        "type": "string",
        "side": "string",
        "quantity": "number",
        "status": "string",
        "filled_quantity": "number",
        "filled_price": "number",
        "created_at": "string",
        "updated_at": "string"
      }
    ]
  }
  ```

### Portfolio
#### Get Portfolio Holdings
- **GET** `/portfolio`
- **Response:** `200 OK`
  ```json
  {
    "holdings": [
      {
        "symbol": "string",
        "shares": "number",
        "average_cost": "number",
        "current_price": "number",
        "market_value": "number",
        "total_return": "number",
        "total_return_percentage": "number"
      }
    ]
  }
  ```

### Watchlist
#### Get Watchlists
- **GET** `/watchlists`
- **Response:** `200 OK`
  ```json
  {
    "watchlists": [
      {
        "id": "string",
        "name": "string",
        "stocks": [
          {
            "symbol": "string",
            "name": "string",
            "current_price": "number",
            "price_change": "number",
            "price_change_percentage": "number"
          }
        ]
      }
    ]
  }
  ```

#### Create Watchlist
- **POST** `/watchlists`
- **Request Body:**
  ```json
  {
    "name": "string",
    "symbols": ["string"]
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "id": "string",
    "name": "string"
  }
  ```

#### Add to Watchlist
- **POST** `/watchlists/{watchlist_id}/stocks`
- **Request Body:**
  ```json
  {
    "symbol": "string"
  }
  ```
- **Response:** `200 OK`

#### Remove from Watchlist
- **DELETE** `/watchlists/{watchlist_id}/stocks/{symbol}`
- **Response:** `204 No Content`

## Error Responses
All endpoints may return the following errors:

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

Error Response Format: