import sqlite3
from models.item_details import ItemDetails


class ItemDetailsRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def setup_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_details (
                id INTEGER PRIMARY KEY,
                name_fr TEXT,
                type_fr TEXT,
                level INTEGER,
                coefficient INTEGER,
                price INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_characteristics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                name TEXT,
                min_value INTEGER,
                max_value INTEGER,
                FOREIGN KEY (item_id) REFERENCES item_details(id)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def save_item_details(self, details: ItemDetails):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO item_details (id, name_fr, type_fr, level, coefficient, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, details.as_tuple())
        cursor.execute(
            "DELETE FROM item_characteristics WHERE item_id = ?", (details.id,))
        cursor.executemany("""
            INSERT INTO item_characteristics (item_id, name, min_value, max_value)
            VALUES (?, ?, ?, ?)
        """, details.characteristics_tuples())
        conn.commit()
        cursor.close()
        conn.close()
