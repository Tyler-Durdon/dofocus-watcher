import sqlite3
from models.dofus_item import DofusItem


class DofusItemsRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def setup_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dofus_items (
                id INTEGER PRIMARY KEY,
                name_fr TEXT,
                type_fr TEXT,
                level INTEGER
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def save_items_batch(self, items):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR REPLACE INTO dofus_items (id, name_fr, type_fr, level)
            VALUES (?, ?, ?, ?)
        """, [item.as_tuple() for item in items])
        conn.commit()
        cursor.close()
        conn.close()
