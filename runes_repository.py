import sqlite3
from models.rune import Rune


class RunesRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def setup_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runes (
                id INTEGER PRIMARY KEY,
                name_fr TEXT,
                characteristic_fr TEXT,
                value INTEGER,
                weight INTEGER,
                price INTEGER,
                date_updated TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def save_runes_batch(self, runes):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR REPLACE INTO runes (id, name_fr, characteristic_fr, value, weight, price, date_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [rune.as_tuple() for rune in runes])
        conn.commit()
        cursor.close()
        conn.close()
