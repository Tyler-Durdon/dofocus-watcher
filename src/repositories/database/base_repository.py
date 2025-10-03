from src.core.database import Database
from typing import Any, List, Tuple


class BaseRepository:
    def __init__(self, database: Database):
        self.database = database

    def execute_query(self, query: str, params: Tuple = ()) -> Any:
        """Exécute une requête SQL avec paramètres"""
        return self.database.execute(
            lambda conn: conn.execute(query, params).fetchall()
        )

    def execute_many(self, query: str, params_list: List[Tuple]) -> None:
        """Exécute une requête SQL avec plusieurs sets de paramètres"""
        self.database.execute(
            lambda conn: conn.executemany(query, params_list)
        )
