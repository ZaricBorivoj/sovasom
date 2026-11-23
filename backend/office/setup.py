"""Migration then atomic runtime initialization; never repairs or resets existing access."""

import argparse
import json
import os
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from dotenv import dotenv_values, unset_key
from pydantic import BaseModel, EmailStr, Field, SecretStr, ValidationError
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from office.accounts.models import Account, Grant, Installation, Membership
from office.config import Settings
from office.database import session_factory


class Bootstrap(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=100)
    password: SecretStr = Field(min_length=12, max_length=1024)


def initialize(settings: Settings, values: dict) -> bool:
    with session_factory(settings.database_url).begin() as db:
        # All initializers serialize, including when the singleton does not exist yet.
        db.execute(text("SELECT pg_advisory_xact_lock(73546001)"))
        if db.get(Installation, 1):
            return False
        initial = Bootstrap.model_validate(values)
        name = initial.display_name.strip()
        if not name:
            raise ValueError("A display name is required")
        account = Account(
            email=str(initial.email).casefold(),
            display_name=name,
            password_hash=PasswordHasher().hash(initial.password.get_secret_value()),
        )
        db.add(account)
        db.flush()
        db.add(Membership(account_id=account.id))
        db.flush()
        db.add_all(
            [
                Grant(account_id=account.id, role="administrator"),
                Grant(account_id=account.id, role="menu_maintainer"),
                Installation(id=1),
            ]
        )
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()
    try:
        settings = Settings(_env_file=None if args.stdin else (args.env_file or ".env"))
        migrations = Config("alembic.ini")
        migrations.attributes["database_url"] = settings.database_url
        command.upgrade(migrations, "head")
        if args.stdin:
            values = json.load(sys.stdin)
        else:
            runtime = {**dotenv_values(args.env_file or ".env", interpolate=False), **os.environ}
            values = {
                "email": runtime.get("INITIAL_EMAIL", ""),
                "display_name": runtime.get("INITIAL_DISPLAY_NAME", ""),
                "password": runtime.get("INITIAL_PASSWORD", ""),
            }
        created = initialize(settings, values)
        path = args.env_file or Path(".env")
        if not args.stdin and path.is_file():
            path.chmod(0o600)
            for key in ("INITIAL_EMAIL", "INITIAL_DISPLAY_NAME", "INITIAL_PASSWORD"):
                if key in dotenv_values(path, interpolate=False):
                    unset_key(path, key)
        print("Office initialized." if created else "Office already initialized; no changes.")
    except ValidationError as error:
        # Only report fixed field guidance: validation details may contain secrets.
        fields = {item["loc"][0] for item in error.errors(include_input=False) if item["loc"]}
        guidance = {
            "email": "INITIAL_EMAIL must be a valid email address.",
            "display_name": "INITIAL_DISPLAY_NAME must contain 1 to 100 characters.",
            "password": "INITIAL_PASSWORD must contain 12 to 1024 characters.",
        }
        messages = [message for field, message in guidance.items() if field in fields]
        print(
            "Setup failed: " + (" ".join(messages) or "Check runtime configuration."),
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    except OperationalError:
        print(
            "Setup failed: Cannot connect to PostgreSQL. Check that DATABASE_PASSWORD "
            "matches the existing database password and PostgreSQL is reachable. "
            "Changing .env does not reset an existing database password.",
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    except Exception:
        # Validation/driver exceptions can contain credentials. Never print their values.
        print(
            "Setup failed. Check runtime configuration and database connectivity.", file=sys.stderr
        )
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
