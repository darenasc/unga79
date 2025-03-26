import sqlite3
from pathlib import Path

import pandas as pd

from unga79.config import DATA_DIR

DB = DATA_DIR / "countries.db"

QUERIES = {
    "create": """CREATE TABLE IF NOT EXISTS countries (
                country TEXT,
                url TEXT,
                full_speech TEXT,
                summary TEXT,
                countries_mentioned TEXT,
                risks TEXT,
                haiku TEXT
                );
                """,
    "insert": """INSERT INTO countries (country, url, full_speech) VALUES (?, ?, ?);""",
    "delete": """DELETE FROM countries where country = ?""",
    "select": """SELECT * FROM countries;""",
    "check": """SELECT * FROM countries where country = ?;""",
    "drop": """DROP TABLE countries;""",
}


def create_db(db: str | Path = DB):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERIES["create"])
        conn.commit
        cursor.close()


def insert(
    country: str, url: str, speech: str, db: str | Path = DB, overwrite: bool = False
):
    if not overwrite:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(QUERIES["check"], (country,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                cursor.close()
                return

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERIES["delete"], (country,))
        conn.commit()
        cursor.execute(QUERIES["insert"], (country, url, speech))
        conn.commit()
        cursor.close()


def select_country(db: str | Path = DB) -> pd.DataFrame:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        rows = cursor.execute(QUERIES["select"]).fetchall()
        column_names = [x[0] for x in cursor.description]
        cursor.close()

    df = pd.DataFrame(rows, columns=column_names)
    return df


def drop_country(db: str | Path = DB) -> pd.DataFrame:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERIES["drop"])
        conn.commit()
        cursor.close()
