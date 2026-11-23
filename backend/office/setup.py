"""Migration then atomic runtime initialization; never repairs or resets existing access."""

import argparse
import json
import os
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from pydantic import BaseModel, EmailStr, Field, SecretStr
from sqlalchemy import text

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
    parser.add_argument("--bootstrap-file", type=Path)
    parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()
    try:
        settings = Settings()
        command.upgrade(Config("alembic.ini"), "head")
        if args.bootstrap_file:
            values = json.loads(args.bootstrap_file.read_text())
        elif args.stdin:
            values = json.load(sys.stdin)
        else:
            values = {
                "email": os.environ.pop("INITIAL_EMAIL", ""),
                "display_name": os.environ.pop("INITIAL_DISPLAY_NAME", ""),
                "password": os.environ.pop("INITIAL_PASSWORD", ""),
            }
        created = initialize(settings, values)
        if args.bootstrap_file:
            args.bootstrap_file.unlink()
        print("Office initialized." if created else "Office already initialized; no changes.")
    except Exception:
        # Validation/driver exceptions can contain credentials. Never print their values.
        print(
            "Setup failed. Check runtime configuration and database connectivity.", file=sys.stderr
        )
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
