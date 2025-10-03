import sqlite3


class DatabaseRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def setup_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                level INTEGER,
                coefficient INTEGER,
                price INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characteristics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                name TEXT,
                min_value INTEGER,
                max_value INTEGER,
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
