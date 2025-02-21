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
  "email": "demo@aa.io"
}
```
- Error Response (401):
```json
{
  "errors": {
    "message": "Unauthorized"
  }
}
```

### Login
- Endpoint: `POST /api/auth/login`
- Request Body:
```json
{
  "email": "demo@aa.io",
  "password": "password"
}
```
- Success Response:
```json
{
  "id": 1,
  "username": "Demo",
  "email": "demo@aa.io"
}
```
- Error Response (401):
```json
{
  "errors": ["Invalid credentials"]
}
```

### Signup
- Endpoint: `POST /api/auth/signup`
- Request Body:
```json
{
  "username": "newuser",
  "email": "new@user.io",
  "password": "password"
}
```
- Success Response:
```json
{
  "id": 2,
  "username": "newuser",
  "email": "new@user.io"
}
```
- Error Response (400):
```json
{
  "errors": {
    "email": "Email already exists",
    "username": "Username already exists"
  }
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

## Orders

### Get User's Orders
- Endpoint: `GET /api/orders`
- Authentication: Required
- Query Parameters:
  - `status`: Filter orders by status (optional)
- Response: List of orders
```json
{
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "symbol": "AAPL",
      "order_type": "market",
      "side": "buy",
      "shares": 10.0,
      "price": 175.50,
      "status": "filled",
      "filled_price": 175.50,
      "filled_at": "2024-01-20T15:30:00Z",
      "created_at": "2024-01-20T15:30:00Z",
      "updated_at": "2024-01-20T15:30:00Z"
    }
  ]
}
```

### Place Order
- Endpoint: `POST /api/orders`
- Authentication: Required
- Request Body:
```json
{
  "symbol": "AAPL",
  "order_type": "market",  // "market" or "limit"
  "side": "buy",          // "buy" or "sell"
  "shares": 10,
  "price": 175.50        // Required for limit orders
}
```
- Response: Created order object

### Process Order (Demo)
- Endpoint: `POST /api/orders/<order_id>/process`
- Authentication: Required
- Description: Processes a pending order, updates portfolio, creates transaction
- Response: Updated order object

### Cancel Order
- Endpoint: `POST /api/orders/<order_id>/cancel`
- Authentication: Required
- Description: Cancels a pending order
- Response: Updated order object

## Watchlists

### Get User's Watchlists
- Endpoint: `GET /api/watchlists`
- Authentication: Required
- Response: List of watchlists

### Create Watchlist
- Endpoint: `POST /api/watchlists`
- Authentication: Required
- Request Body:
```json
{
  "name": "Tech Stocks",
  "symbols": "AAPL,GOOGL,MSFT"
}
```

### Update Watchlist
- Endpoint: `PUT /api/watchlists/<int:id>`
- Authentication: Required
- Request Body: Same as create

### Delete Watchlist
- Endpoint: `DELETE /api/watchlists/<int:id>`
- Authentication: Required

## Portfolio

### Get Portfolio
- Endpoint: `GET /api/portfolio`
- Authentication: Required
- Response: List of portfolio positions

## Transactions

### Get User's Transactions
- Endpoint: `GET /api/transactions`
- Authentication: Required
- Response:
```json
{
  "transactions": [
    {
      "id": 1,
      "user_id": 1,
      "order_id": 1,
      "symbol": "AAPL",
      "shares": 10.0,
      "price": 175.50,
      "type": "buy",
      "created_at": "2024-01-20T15:30:00Z"
    }
  ]
}
```

