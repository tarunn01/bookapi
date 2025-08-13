import os
import time
import psycopg2
from urllib.parse import urlparse


def build_dsn_from_env() -> str:
    # Prefer DATABASE_URL if provided; otherwise build from POSTGRES_* variables
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    user = os.getenv("POSTGRES_USER", "flaskuser")
    password = os.getenv("POSTGRES_PASSWORD", "flaskpass")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    dbname = os.getenv("POSTGRES_DB", "flaskdb")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def wait_for_db(max_attempts: int = 60, delay_seconds: float = 1.0) -> None:
    dsn = build_dsn_from_env()
    for attempt in range(1, max_attempts + 1):
        try:
            conn = psycopg2.connect(dsn)
            conn.close()
            print("Database is ready")
            return
        except Exception as exc:  # noqa: BLE001
            print(f"Waiting for database... attempt {attempt}/{max_attempts}: {exc}")
            time.sleep(delay_seconds)
    raise TimeoutError("Database not ready after waiting")


if __name__ == "__main__":
    attempts = int(os.getenv("DB_MAX_ATTEMPTS", "60"))
    delay = float(os.getenv("DB_WAIT_DELAY", "1.0"))
    wait_for_db(attempts, delay)