from __future__ import annotations
import os
import sqlite3
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: int
    name: str

def get_db_path() -> str:
    return os.environ.get("APP_DB_PATH", "/tmp/app.db")

def init_db() -> None:
    path = get_db_path()
    con = sqlite3.connect(path)
    try:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        con.commit()
    finally:
        con.close()

def add_user(name: str) -> int:
    if not name or not name.strip():
        raise ValueError("name must be non-empty")
    con = sqlite3.connect(get_db_path())
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO users(name) VALUES (?)", (name.strip(),))
        con.commit()
        return int(cur.lastrowid)
    finally:
        con.close()

def get_user(user_id: int) -> User | None:
    con = sqlite3.connect(get_db_path())
    try:
        cur = con.cursor()
        cur.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return User(id=int(row[0]), name=str(row[1]))
    finally:
        con.close()
