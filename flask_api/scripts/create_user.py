import argparse
import os

from app import create_app
from app.extensions import db
from app.models import User


def main():
    parser = argparse.ArgumentParser(description="Create a user in the database")
    parser.add_argument("--email", required=True, help="User email")
    parser.add_argument("--name", required=True, help="User full name")
    parser.add_argument("--password", required=True, help="User password")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        existing = User.query.filter_by(email=args.email.lower()).first()
        if existing:
            print("User already exists:", existing.email)
            return
        user = User(email=args.email.lower(), name=args.name)
        user.set_password(args.password)
        db.session.add(user)
        db.session.commit()
        print("Created user:", user.id, user.email)


if __name__ == "__main__":
    main()