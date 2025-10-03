import sqlite3
from typing import Callable, Any

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute(self, operation: Callable, *args, **kwargs) -> Any:
        """Execute une opération dans un contexte de connection sécurisé"""
        with self.connect() as conn:
            try:
                result = operation(conn, *args, **kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e

    def setup_database(self):
        """Initialise toutes les tables nécessaires"""
        self.execute(lambda conn: conn.executescript("""
            CREATE TABLE IF NOT EXISTS dofus_items (
                id INTEGER PRIMARY KEY,
                name_fr TEXT,
                type_fr TEXT,
                level INTEGER
            );

            CREATE TABLE IF NOT EXISTS item_details (
                id INTEGER PRIMARY KEY,
                name_fr TEXT,
                type_fr TEXT,
                level INTEGER,
                coefficient REAL,
                price REAL
            );

            CREATE TABLE IF NOT EXISTS item_characteristics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                name TEXT,
                min_value INTEGER,
                max_value INTEGER,
                FOREIGN KEY (item_id) REFERENCES item_details(id)
            );

            CREATE TABLE IF NOT EXISTS runes (
                id INTEGER PRIMARY KEY,
                name_fr TEXT,
                characteristic_fr TEXT,
                value INTEGER,
                weight INTEGER,
                price REAL,
                date_updated TEXT
            );

            CREATE TABLE IF NOT EXISTS break_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                item_name TEXT,
                characteristic TEXT,
                rune_name TEXT,
                runes_generated REAL,
                rune_price REAL,
                best_rune TEXT
            );
        """))
