import json
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

from palisade import config
from palisade.db.models import Filter

SCHEMA = """
CREATE TABLE IF NOT EXISTS filters (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    schedule_json TEXT NOT NULL,
    blocked_websites_json TEXT NOT NULL,
    blocked_apps_json TEXT NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def init_db() -> None:
    config.db_path().parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA)


@contextmanager
def connect() -> Generator[sqlite3.Connection]:
    conn = sqlite3.connect(str(config.db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def create_filter(f: Filter) -> None:
    with connect() as conn:
        conn.execute(
            """INSERT INTO filters
            (id, name, schedule_json, blocked_websites_json, blocked_apps_json,
             enabled, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            f.to_row(),
        )


def update_filter(f: Filter) -> None:
    with connect() as conn:
        conn.execute(
            """UPDATE filters
            SET name = ?, schedule_json = ?, blocked_websites_json = ?,
                blocked_apps_json = ?, enabled = ?
            WHERE id = ?""",
            (
                f.name,
                f.schedule.to_json(),
                json.dumps(f.blocked_websites),
                json.dumps(f.blocked_apps),
                1 if f.enabled else 0,
                f.id,
            ),
        )


def get_filter(filter_id: str) -> Filter | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM filters WHERE id = ?", (filter_id,)
        ).fetchone()
    return Filter.from_row(row) if row else None


def list_filters() -> list[Filter]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM filters ORDER BY created_at ASC").fetchall()
    return [Filter.from_row(r) for r in rows]


def delete_filter(filter_id: str) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM filters WHERE id = ?", (filter_id,))


def get_setting(key: str, default: str | None = None) -> str | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    with connect() as conn:
        conn.execute(
            """INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value""",
            (key, value),
        )
