import sqlite3
from models.break_result import BreakResult


class BreakResultsRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def setup_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS break_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                item_name TEXT,
                characteristic TEXT,
                rune_name TEXT,
                runes_generated REAL,
                rune_price REAL,
                best_rune TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def save_results_batch(self, results):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO break_results (
                item_id, item_name, characteristic, rune_name, runes_generated, rune_price, best_rune
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [result.as_tuple() for result in results])
        conn.commit()
        cursor.close()
        conn.close()
