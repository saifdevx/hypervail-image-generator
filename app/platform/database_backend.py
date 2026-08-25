import os
import sqlite3
from pathlib import Path
from typing import Protocol


class DatabaseBackend(Protocol):
    name: str

    def connect(self):
        ...


class SQLiteDatabaseBackend:
    name = "sqlite"

    def __init__(
        self,
        database_path: Path,
    ):
        self.database_path = (
            database_path
        )

    def connect(self):
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = (
            sqlite3.Row
        )

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection


class TursoDatabaseBackend:
    """
    Phase 1 interface placeholder.

    Phase 2 will activate the remote Turso driver after the local
    ownership/admin/model-registry migration is proven stable.
    """

    name = "turso"

    def connect(self):
        raise RuntimeError(
            "DATABASE_PROVIDER=turso is reserved for "
            "Hyperex Step 14 Phase 2. Keep DATABASE_PROVIDER=sqlite "
            "during Phase 1."
        )


def get_database_backend(
    database_path: Path,
):
    provider = (
        os.getenv(
            "DATABASE_PROVIDER",
            "sqlite",
        )
        or
        "sqlite"
    ).strip().lower()

    if provider == "turso":
        return TursoDatabaseBackend()

    return SQLiteDatabaseBackend(
        database_path
    )
