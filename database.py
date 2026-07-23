"""
database.py
Camada de conexão com o banco de dados (SQLite).
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tarefas.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Recria o banco de dados a partir do schema.sql."""
    with get_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    print(f"Banco de dados inicializado em: {DB_PATH}")


if __name__ == "__main__":
    init_db()
