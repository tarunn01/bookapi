import os
import json

# Force SQLite for quick smoke testing
os.environ["DATABASE_URL"] = "sqlite:///test.db"

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import User  # noqa: E402


def assert_status(resp, expected):
    if resp.status_code != expected:
        raise SystemExit(f"Expected status {expected}, got {resp.status_code}, body={resp.get_data(as_text=True)}")


def main():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Seed a user to log in
        admin = User(email="admin@example.com", name="Admin")
        admin.set_password("password123")
        db.session.add(admin)
        db.session.commit()

        client = app.test_client()

        # Login
        r = client.post(
            "/auth/login",
            json={"email": "admin@example.com", "password": "password123"},
        )
        assert_status(r, 200)
        data = r.get_json()
        access = data["access_token"]
        headers = {"Authorization": f"Bearer {access}"}

        # Create user
        r = client.post(
            "/users",
            json={
                "email": "alice@example.com",
                "name": "Alice",
                "password": "testpass123",
            },
            headers=headers,
        )
        assert_status(r, 201)
        alice = r.get_json()
        alice_id = alice["id"]

        # List users
        r = client.get("/users", headers=headers)
        assert_status(r, 200)
        users = r.get_json()
        assert any(u["email"] == "alice@example.com" for u in users)

        # Get one
        r = client.get(f"/users/{alice_id}", headers=headers)
        assert_status(r, 200)

        # Update
        r = client.put(
            f"/users/{alice_id}",
            json={"name": "Alice Updated"},
            headers=headers,
        )
        assert_status(r, 200)
        assert r.get_json()["name"] == "Alice Updated"

        # Delete
        r = client.delete(f"/users/{alice_id}", headers=headers)
        assert_status(r, 200)

        print("SMOKE TEST PASSED")


if __name__ == "__main__":
    main()