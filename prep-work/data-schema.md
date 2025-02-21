# Database Schema

## Users (`users`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| username | String | Unique, Not Null |
| email | String | Unique, Not Null |
| hashed_password | String | Not Null |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Orders (`orders`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| symbol | String(10) | Not Null |
| order_type | String(10) | Not Null ('market' or 'limit') |
| side | String(4) | Not Null ('buy' or 'sell') |
| shares | Float | Not Null |
| price | Float | Nullable (Required for limit orders) |
| status | String(10) | Not Null ('pending', 'filled', 'cancelled') |
| filled_price | Float | Nullable |
| filled_at | DateTime | Nullable |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Portfolios (`portfolios`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| symbol | String(10) | Not Null |
| shares | Float | Not Null |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Transactions (`transactions`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| order_id | Integer | Foreign Key (orders.id), Not Null |
| symbol | String(10) | Not Null |
| shares | Float | Not Null |
| price | Float | Not Null |
| type | String(4) | Not Null ('buy' or 'sell') |
| created_at | DateTime | Not Null, Default: now() |

## Watchlists (`watchlists`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| name | String | Not Null |
| symbols | String | Not Null (comma-separated list) |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Relationships
- User has many Orders (one-to-many)
- User has many Portfolios (one-to-many)
- User has many Transactions (one-to-many)
- User has many Watchlists (one-to-many)
- Order belongs to User (many-to-one)
- Order has one Transaction (one-to-one)
- Portfolio belongs to User (many-to-one)
- Transaction belongs to User and Order (many-to-one)
- Watchlist belongs to User (many-to-one)

## Notes
1. All DateTime fields use UTC timezone
2. All Float fields store decimal numbers for precision
3. Foreign keys have appropriate indexes for performance
4. All tables use the production schema prefix when deployed
5. Symbols are standardized to uppercase
6. Status fields use predefined string values
7. Soft deletes are not implemented (records are permanently deleted) 