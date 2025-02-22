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
| created_at | DateTime | Not Null, Default: now() |
| updated_at | DateTime | Not Null, Default: now() |

[Rest of the schema remains the same...] 