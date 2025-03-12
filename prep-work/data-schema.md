# Database Schema

## Users (`users`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| username | String | Unique, Not Null |
| first_name | String | Not Null |
| last_name | String | Not Null |
| email | String | Unique, Not Null |
| hashed_password | String | Not Null |
| balance | Float | Not Null, Default: 10000.00 |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Symbols (`symbols`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| symbol | String(10) | Unique, Not Null |
| company_name | String(255) | Not Null |
| current_price | Float | Not Null |
| daily_high | Float | Nullable |
| daily_low | Float | Nullable |
| daily_volume | BigInteger | Nullable |
| price_change_pct | Float | Nullable |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Symbol Prices (`symbol_prices`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| symbol_id | Integer | Foreign Key (symbols.id), Not Null |
| date | Date | Not Null |
| open_price | Float | Not Null |
| close_price | Float | Not Null |
| high_price | Float | Not Null |
| low_price | Float | Not Null |
| volume | BigInteger | Not Null |
| created_at | DateTime | Not Null, Default: now() |

## Orders (`orders`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| symbol_id | Integer | Foreign Key (symbols.id), Not Null |
| shares | Float | Not Null |
| type | String(4) | Not Null ('buy' or 'sell') |
| status | String(10) | Not Null ('pending', 'completed', 'cancelled'), Default: 'pending' |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Portfolios (`portfolios`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| symbol_id | Integer | Foreign Key (symbols.id), Not Null |
| shares | Float | Not Null, Default: 0 |
| average_price | Float | Not Null |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Transactions (`transactions`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| order_id | Integer | Foreign Key (orders.id), Nullable |
| symbol_id | Integer | Foreign Key (symbols.id), Not Null |
| shares | Float | Not Null |
| price | Float | Not Null |
| type | String(4) | Not Null ('buy' or 'sell') |
| created_at | DateTime | Not Null, Default: now() |

## Watchlists (`watchlists`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id), Not Null |
| name | String(50) | Not Null |
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

## Watchlist Symbols (`watchlist_symbols`)
| Column Name | Type | Constraints |
|------------|------|-------------|
| id | Integer | Primary Key |
| watchlist_id | Integer | Foreign Key (watchlists.id), Not Null |
| symbol_id | Integer | Foreign Key (symbols.id), Not Null |
| created_at | DateTime | Not Null, Default: now() |
| UniqueConstraint | | ('watchlist_id', 'symbol_id') |

## Relationships
- User has many Orders (one-to-many)
- User has 1 Portfolios (one-to-one)
- User has many Transactions (one-to-many)
- User has many Watchlists (one-to-many)
- Symbol has many SymbolPrices (one-to-many)
- Symbol has many Portfolio positions (one-to-many)
- Symbol has many Transactions (one-to-many)
- Symbol has many Orders (one-to-many)
- Symbol has many WatchlistSymbols (one-to-many)
- Order belongs to User (many-to-one)
- Order belongs to Symbol (many-to-one)
- Order has many Transactions (one-to-many)
- Portfolio belongs to User (one-to-one)
- Portfolio belongs to Symbol (many-to-one)
- Transaction belongs to User (many-to-one)
- Transaction belongs to Order (many-to-one, optional)
- Transaction belongs to Symbol (many-to-one)
- Watchlist belongs to User (many-to-one)
- Watchlist has many WatchlistSymbols (one-to-many)
- WatchlistSymbol belongs to Watchlist (many-to-one)
- WatchlistSymbol belongs to Symbol (many-to-one)

## Notes
1. All DateTime fields use UTC timezone
2. All Float fields store decimal numbers for precision
3. Foreign keys have appropriate indexes for performance
4. All tables use the production schema prefix when deployed
5. Symbols are standardized to uppercase
6. Status fields use predefined string values
7. Cascade delete is implemented for related records 