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
    "drop": """DROP TABLE countries;""",
}


def create_db(db: str | Path = DB):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERIES["create"])
        conn.commit
        cursor.close()


def insert(country: str, url: str, speech: str, db: str | Path = DB):
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
