# Flask REST API (Users CRUD) with JWT, Marshmallow, SQLAlchemy, Postgres, Docker

## Quickstart

1. Copy env file and edit secrets as needed:

```bash
cp .env.example .env
```

2. Build and run:

```bash
docker compose up --build
```

App runs on http://localhost:8000

3. Create an initial user (so you can log in):

```bash
docker compose exec web python scripts/create_user.py --email admin@example.com --name "Admin" --password password123
```

4. Login and call protected endpoints:

```bash
# Login
curl -s -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"password123"}' | tee /tmp/jwt.json

# Extract access token (jq recommended)
ACCESS=$(cat /tmp/jwt.json | python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])')

# Create user
curl -s -X POST http://localhost:8000/users \
  -H "Authorization: Bearer $ACCESS" \
  -H 'Content-Type: application/json' \
  -d '{"email":"alice@example.com","name":"Alice","password":"testpass123"}'

# List users
curl -s -H "Authorization: Bearer $ACCESS" http://localhost:8000/users
```

## Endpoints

- POST `/auth/login` — login with email/password, returns access and refresh JWTs
- POST `/auth/refresh` — refresh access token using refresh token
- GET `/users` — list users (JWT required)
- POST `/users` — create user (JWT required)
- GET `/users/<id>` — retrieve user by id (JWT required)
- PUT `/users/<id>` — update user (JWT required)
- DELETE `/users/<id>` — delete user (JWT required)

Bodies are validated with Marshmallow. Passwords are hashed.

## OAuth (optional, scaffolded)

Google OAuth routes are scaffolded at:
- GET `/oauth/login/google`
- GET `/oauth/callback/google`

Set `OAUTH_GOOGLE_CLIENT_ID`, `OAUTH_GOOGLE_CLIENT_SECRET`, and `OAUTH_REDIRECT_URI` in `.env`. When configured, Google login will create or match a user by email and issue your API's JWT.

## Notes

- Database tables are auto-created on startup if missing.
- Default Docker network hostname for Postgres is `db`.