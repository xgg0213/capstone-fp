# API Documentation

## Authentication

### Get Current User
- Endpoint: `GET /api/auth`
- Authentication: Required
- Response:
```json
{
  "id": 1,
  "username": "Demo",
  "first_name": "Demo",
  "last_name": "User",
  "email": "demo@aa.io",
  "balance": 10000.00
}
```

### Signup
- Endpoint: `POST /api/auth/signup`
- Request Body:
```json
{
  "username": "newuser",
  "first_name": "New",
  "last_name": "User",
  "email": "new@user.io",
  "password": "password"
}
```
- Success Response:
```json
{
  "id": 2,
  "username": "newuser",
  "first_name": "New",
  "last_name": "User",
  "email": "new@user.io",
  "balance": 10000.00
}
```
- Error Response (400):
```json
{
  "errors": {
    "email": ["Email address already in use"],
    "username": ["Username already in use"]
  }
}
```

### Login
- Endpoint: `POST /api/auth/login`
- Request Body:
```json
{
  "credential": "demo@aa.io",
  "password": "password"
}
```
- Success Response:
```json
{
  "id": 1,
  "username": "Demo",
  "first_name": "Demo",
  "last_name": "User",
  "email": "demo@aa.io",
  "balance": 10000.00
}
```
- Error Response (401):
```json
{
  "errors": ["Invalid credentials"]
}
```

### Logout
- Endpoint: `POST /api/auth/logout`
- Authentication: Required
- Response:
```json
{
  "message": "User logged out"
}
```

## Symbols

### Get All Symbols
- Endpoint: `GET /api/symbols`
- Authentication: Required
- Response:
```json
{
  "symbols": [
    {
      "id": 1,
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "current_price": 175.50,
      "daily_high": 178.20,
      "daily_low": 174.80,
      "daily_volume": 75000000,
      "price_change_pct": 1.25,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "price_history": [
        {
          "id": 1,
          "date": "2023-01-01",
          "open_price": 174.50,
          "close_price": 175.50,
          "high_price": 178.20,
          "low_price": 174.80,
          "volume": 75000000
        }
      ]
    }
  ]
}
```

### Get Symbol Details
- Endpoint: `GET /api/symbols/:symbol`
- Authentication: Required
- Response:
```json
{
  "id": 1,
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "current_price": 175.50,
  "daily_high": 178.20,
  "daily_low": 174.80,
  "daily_volume": 75000000,
  "price_change_pct": 1.25,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "price_history": [
    {
      "id": 1,
      "date": "2023-01-01",
      "open_price": 174.50,
      "close_price": 175.50,
      "high_price": 178.20,
      "low_price": 174.80,
      "volume": 75000000
    }
  ]
}
```

### Get Symbol Price History
- Endpoint: `GET /api/symbols/:symbol/prices`
- Authentication: Required
- Response:
```json
[
  {
    "id": 1,
    "date": "2023-01-01",
    "open_price": 174.50,
    "close_price": 175.50,
    "high_price": 178.20,
    "low_price": 174.80,
    "volume": 75000000
  }
]
```

## Portfolio

### Get User Portfolio
- Endpoint: `GET /api/portfolio`
- Authentication: Required
- Response:
```json
{
  "portfolios": [
    {
      "id": 1,
      "user_id": 1,
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "shares": 10.0,
      "average_price": 150.00,
      "current_price": 175.50,
      "market_value": 1755.00,
      "total_cost": 1500.00,
      "total_return": 17.00,
      "day_change": 1.25,
      "unrealized_gain": 255.00,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

### Get Portfolio History
- Endpoint: `GET /api/portfolio/history`
- Authentication: Required
- Response:
```json
{
  "history": [
    {
      "timestamp": "2023-01-01T00:00:00Z",
      "value": 1500.00
    }
  ]
}
```

## Orders

### Place Order
- Endpoint: `POST /api/orders`
- Authentication: Required
- Request Body:
```json
{
  "symbol": "AAPL",
  "shares": 5.0,
  "type": "buy",
  "price": 175.50
}
```
- Success Response:
```json
{
  "id": 1,
  "user_id": 1,
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "shares": 5.0,
  "type": "buy",
  "status": "completed",
  "current_price": 175.50,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "transactions": [
    {
      "id": 1,
      "user_id": 1,
      "order_id": 1,
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "shares": 5.0,
      "price": 175.50,
      "type": "buy",
      "total": 877.50,
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```
- Error Response (400):
```json
{
  "error": "Insufficient funds"
}
```

### Get User Orders
- Endpoint: `GET /api/orders`
- Authentication: Required
- Query Parameters:
  - `status`: Filter by status (pending, completed, cancelled)
- Response:
```json
{
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "shares": 5.0,
      "type": "buy",
      "status": "completed",
      "current_price": 175.50,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "transactions": [
        {
          "id": 1,
          "user_id": 1,
          "order_id": 1,
          "symbol": "AAPL",
          "company_name": "Apple Inc.",
          "shares": 5.0,
          "price": 175.50,
          "type": "buy",
          "total": 877.50,
          "created_at": "2023-01-01T00:00:00Z"
        }
      ]
    }
  ]
}
```

### Cancel Order
- Endpoint: `POST /api/orders/:id/cancel`
- Authentication: Required
- Response:
```json
{
  "id": 1,
  "user_id": 1,
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "shares": 5.0,
  "type": "buy",
  "status": "cancelled",
  "current_price": 175.50,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "transactions": []
}
```

## Transactions

### Get User Transactions
- Endpoint: `GET /api/transactions`
- Authentication: Required
- Query Parameters:
  - `symbol`: Filter by symbol
  - `type`: Filter by type (buy, sell)
- Response:
```json
{
  "transactions": [
    {
      "id": 1,
      "user_id": 1,
      "order_id": 1,
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "shares": 5.0,
      "price": 175.50,
      "current_price": 180.00,
      "type": "buy",
      "total": 877.50,
      "gain_loss": null,
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

### Get Transaction Statistics
- Endpoint: `GET /api/transactions/stats`
- Authentication: Required
- Query Parameters:
  - `symbol`: Required, filter by symbol
- Response:
```json
{
  "total_bought": 10.0,
  "total_sold": 5.0,
  "average_buy_price": 170.00,
  "average_sell_price": 180.00,
  "total_spent": 1700.00,
  "total_received": 900.00,
  "realized_gain_loss": 50.00
}
```

## Watchlists

### Get User Watchlists
- Endpoint: `GET /api/watchlist`
- Authentication: Required
- Response:
```json
{
  "watchlists": [
    {
      "id": 1,
      "user_id": 1,
      "name": "Tech Stocks",
      "symbols": [
        {
          "id": 1,
          "symbol": "AAPL",
          "company_name": "Apple Inc.",
          "current_price": 175.50,
          "price_change": 1.25
        }
      ],
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

### Create Watchlist
- Endpoint: `POST /api/watchlist`
- Authentication: Required
- Request Body:
```json
{
  "name": "Tech Stocks"
}
```
- Response:
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Tech Stocks",
  "symbols": [],
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Add Symbol to Watchlist
- Endpoint: `POST /api/watchlist/:id/symbols`
- Authentication: Required
- Request Body:
```json
{
  "symbol": "AAPL"
}
```
- Response:
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Tech Stocks",
  "symbols": [
    {
      "id": 1,
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "current_price": 175.50,
      "price_change": 1.25
    }
  ],
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Remove Symbol from Watchlist
- Endpoint: `DELETE /api/watchlist/:id/symbols/:symbol`
- Authentication: Required
- Response:
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Tech Stocks",
  "symbols": [],
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Delete Watchlist
- Endpoint: `DELETE /api/watchlist/:id`
- Authentication: Required
- Response:
```json
{
  "message": "Watchlist deleted successfully"
}
```

