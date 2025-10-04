from typing import List
from src.core.database import Database
from src.models.item import Item


class DofusItemsRepository:
    def __init__(self, database: Database):
        self.database = database

    def save_items_batch(self, items: List[Item]) -> None:
        self.database.execute(
            lambda conn: conn.executemany("""
                INSERT OR REPLACE INTO dofus_items (id, name_fr, type_fr, level)
                VALUES (?, ?, ?, ?)
            """, [(item.id, item.name_fr, item.type_fr, item.level) for item in items])
        )

    def get_all_items(self) -> List[Item]:
        return self.database.execute(
            lambda conn: [
                Item(id=row[0], name_fr=row[1], type_fr=row[2], level=row[3])
                for row in conn.execute(
                    "SELECT id, name_fr, type_fr, level FROM dofus_items"
                ).fetchall()
            ]
        )
