import os
import sqlite3
from pathlib import Path
from typing import Protocol


class DatabaseBackend(Protocol):
    name: str

    def connect(self):
        ...


class MappingRow:
    """Small sqlite3.Row-compatible wrapper for remote Turso cursors."""

    def __init__(self, columns, values):
        self._columns = list(columns)
        self._values = list(values)
        self._mapping = {
            name: value
            for name, value in zip(self._columns, self._values)
        }

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return self._mapping[key]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._values)

    def keys(self):
        return self._mapping.keys()

    def items(self):
        return self._mapping.items()

    def values(self):
        return self._mapping.values()


class CursorAdapter:
    def __init__(self, cursor):
        self._cursor = cursor

    @property
    def description(self):
        return getattr(self._cursor, "description", None)

    @property
    def lastrowid(self):
        return getattr(self._cursor, "lastrowid", None)

    @property
    def rowcount(self):
        value = getattr(self._cursor, "rowcount", -1)
        return -1 if value is None else value

    def execute(self, sql, params=()):
        self._cursor.execute(sql, params)
        return self

    def executemany(self, sql, seq_of_params):
        self._cursor.executemany(sql, seq_of_params)
        return self

    def _convert(self, row):
        if row is None:
            return None

        if isinstance(row, sqlite3.Row):
            return row

        if isinstance(row, dict):
            return row

        if hasattr(row, "keys"):
            try:
                return row
            except Exception:
                pass

        description = self.description or []
        columns = [
            item[0] if isinstance(item, (tuple, list)) else str(item)
            for item in description
        ]

        if not columns:
            return row

        return MappingRow(columns, row)

    def fetchone(self):
        return self._convert(self._cursor.fetchone())

    def fetchall(self):
        return [self._convert(row) for row in self._cursor.fetchall()]

    def __iter__(self):
        for row in self._cursor:
            yield self._convert(row)


class ConnectionAdapter:
    """Normalizes sqlite3 and Turso DB-API behavior used by Hyperex."""

    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return CursorAdapter(self._connection.cursor())

    def execute(self, sql, params=()):
        return CursorAdapter(self._connection.execute(sql, params))

    def executemany(self, sql, seq_of_params):
        if hasattr(self._connection, "executemany"):
            return CursorAdapter(self._connection.executemany(sql, seq_of_params))

        cursor = self.cursor()
        for params in seq_of_params:
            cursor.execute(sql, params)
        return cursor

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        if hasattr(self._connection, "rollback"):
            return self._connection.rollback()
        return None

    def close(self):
        return self._connection.close()


class SQLiteDatabaseBackend:
    name = "sqlite"

    def __init__(self, database_path: Path):
        self.database_path = database_path

    def connect(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return ConnectionAdapter(connection)


class TursoDatabaseBackend:
    name = "turso"

    def __init__(self):
        self.database_url = (os.getenv("TURSO_DATABASE_URL") or "").strip()
        self.auth_token = (os.getenv("TURSO_AUTH_TOKEN") or "").strip()

    def connect(self):
        if not self.database_url or not self.auth_token:
            raise RuntimeError(
                "DATABASE_PROVIDER=turso requires TURSO_DATABASE_URL and TURSO_AUTH_TOKEN."
            )

        try:
            import libsql
        except ImportError as error:
            raise RuntimeError(
                "Turso is selected but the 'libsql' Python package is not installed. "
                "Run: pip install libsql"
            ) from error

        connection = libsql.connect(
            database=self.database_url,
            auth_token=self.auth_token,
        )

        return ConnectionAdapter(connection)


def get_database_provider():
    provider = (os.getenv("DATABASE_PROVIDER", "sqlite") or "sqlite").strip().lower()
    return provider if provider in {"sqlite", "turso"} else "sqlite"


def database_is_configured():
    provider = get_database_provider()
    if provider == "sqlite":
        return True
    return bool(
        (os.getenv("TURSO_DATABASE_URL") or "").strip()
        and (os.getenv("TURSO_AUTH_TOKEN") or "").strip()
    )


def get_database_backend(database_path: Path):
    if get_database_provider() == "turso":
        return TursoDatabaseBackend()
    return SQLiteDatabaseBackend(database_path)
