# Hidden Gems Database Notes

The app uses a local SQLite database named `hidden_gems.db`, created in the project root on first run.

## Tables

### 1. `users`

Stores accounts for email login. Login is only allowed when `email_verified` is 1.

| Column         | Type    | Description                    |
|----------------|---------|--------------------------------|
| id             | INTEGER | Primary key, auto-increment    |
| email          | TEXT    | Unique, not null               |
| password_hash  | TEXT    | SHA-256 hash (salted), not null|
| email_verified | INTEGER | 1 = verified, 0 = pending (must verify before login) |
| created_at     | TEXT    | ISO datetime, default now      |

---

### 2. `email_verification_codes`

Stores verification codes for email verification after registration (or when resending). In the default setup the code is shown on-screen; with email configured it is sent by email.

| Column      | Type    | Description        |
|-------------|---------|--------------------|
| id          | INTEGER | Primary key        |
| user_id     | INTEGER | FK → users.id      |
| code        | TEXT    | 6-digit code       |
| created_at  | TEXT    | ISO datetime       |

---

### 3. `verification_attempts`

Stores verification attempts so you can track bot-prevention activity. Used at login (and can be used before review/favorite actions).

| Column          | Type    | Description                                  |
|-----------------|---------|----------------------------------------------|
| id              | INTEGER | Primary key, auto-increment                  |
| email           | TEXT    | Email of user who attempted (if login)       |
| verification_type| TEXT   | `"math"` or `"code"`                         |
| question        | TEXT    | e.g. "What is 7 + 3?" or "Enter the code: AB12" |
| correct_answer  | TEXT    | Expected answer                              |
| user_answer     | TEXT    | What the user entered                        |
| success         | INTEGER | 1 = correct, 0 = incorrect                   |
| attempted_at    | TEXT    | ISO datetime of attempt                      |
| context         | TEXT    | e.g. `"login"`, `"review"`, `"favorite"`     |

**How to view:** In the app: Main Menu → **View Verification Table (DB Records)**. You can also open `hidden_gems.db` with a SQLite browser and query `verification_attempts`.

---

### 4. `businesses`

Local business directory.

| Column          | Type    | Description                    |
|-----------------|---------|--------------------------------|
| id              | INTEGER | Primary key                    |
| name            | TEXT    | Business name                  |
| category        | TEXT    | e.g. Food, Retail, Services    |
| description     | TEXT    | Short description              |
| average_rating  | REAL    | Computed from reviews          |
| total_reviews   | INTEGER | Count of reviews               |

---

### 5. `deals`

Special deals or promotions for a business.

| Column      | Type    | Description        |
|-------------|---------|--------------------|
| id          | INTEGER | Primary key        |
| business_id | INTEGER | FK → businesses.id |
| description | TEXT    | Deal text          |

---

### 6. `reviews`

User reviews for businesses (linked to logged-in user).

| Column       | Type    | Description        |
|--------------|---------|--------------------|
| id           | INTEGER | Primary key        |
| business_id  | INTEGER | FK → businesses.id |
| user_id      | INTEGER | FK → users.id      |
| rating       | INTEGER | 1–5                |
| review_text  | TEXT    | Review content     |
| created_date | TEXT    | Date of review     |
| created_time | TEXT    | Time of review     |

---

### 7. `favorites`

User bookmarks (user_id + business_id).

| Column      | Type    | Description        |
|-------------|---------|--------------------|
| id          | INTEGER | Primary key        |
| user_id     | INTEGER | FK → users.id      |
| business_id | INTEGER | FK → businesses.id |
| UNIQUE(user_id, business_id) | | One favorite per user per business |

---

## Relationships

- **users** ← reviews, favorites, email_verification_codes.
- **businesses** ← reviews, favorites, deals.
- **verification_attempts** and **email_verification_codes** are used for login/email verification.

Data persists between sessions; the app does not require internet.
