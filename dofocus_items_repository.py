import sqlite3
from models.dofocus_item import DofocusItem


class DofocusItemsRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def setup_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dofocus_items (
                id INTEGER PRIMARY KEY,
                name_fr TEXT,
                name_en TEXT,
                name_es TEXT,
                type_fr TEXT,
                type_en TEXT,
                type_es TEXT,
                level INTEGER,
                price INTEGER,
                img TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def save_item(self, item: DofocusItem):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO dofocus_items (
                id, name_fr, name_en, name_es,
                type_fr, type_en, type_es,
                level, price, img
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, item.as_tuple())
        conn.commit()
        cursor.close()
        conn.close()
