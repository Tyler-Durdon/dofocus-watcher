from typing import List, Optional
from src.core.database import Database
from src.models.item import Item, Characteristic


class ItemsRepository:
    def __init__(self, database: Database):
        self.database = database

    def save_item(self, item: Item) -> None:
        self.database.execute(lambda conn: conn.execute("""
            INSERT OR REPLACE INTO dofus_items (id, name_fr, type_fr, level)
            VALUES (?, ?, ?, ?)
        """, (item.id, item.name_fr, item.type_fr, item.level)))

    def save_item_details(self, item: Item) -> None:
        def save_details(conn):
            conn.execute("""
                INSERT OR REPLACE INTO item_details 
                (id, name_fr, type_fr, level, coefficient, price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (item.id, item.name_fr, item.type_fr, item.level,
                  item.coefficient, item.price))

            if item.characteristics:
                conn.execute("DELETE FROM item_characteristics WHERE item_id = ?",
                             (item.id,))
                conn.executemany("""
                    INSERT INTO item_characteristics 
                    (item_id, name, min_value, max_value)
                    VALUES (?, ?, ?, ?)
                """, [(item.id, c.name, c.min_value, c.max_value)
                      for c in item.characteristics])

        self.database.execute(save_details)

    def save_item_details_with_dates(self, item: Item, coeff_date: str, price_date: str) -> None:
        def save_details(conn):
            conn.execute("""
                INSERT OR REPLACE INTO item_details 
                (id, name_fr, type_fr, level, coefficient, price, coeff_updated_at, price_updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (item.id, item.name_fr, item.type_fr, item.level,
                  item.coefficient, item.price, coeff_date, price_date))

        self.database.execute(save_details)

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        def get_item(conn):
            item_row = conn.execute("""
                SELECT id, name_fr, type_fr, level, coefficient, price 
                FROM item_details WHERE id = ?
            """, (item_id,)).fetchone()

            if not item_row:
                return None

            characteristics = conn.execute("""
                SELECT name, min_value, max_value 
                FROM item_characteristics 
                WHERE item_id = ?
            """, (item_id,)).fetchall()

            return Item(
                id=item_row[0],
                name_fr=item_row[1],
                type_fr=item_row[2],
                level=item_row[3],
                coefficient=item_row[4],
                price=item_row[5],
                characteristics=[
                    Characteristic(name=c[0], min_value=c[1], max_value=c[2])
                    for c in characteristics
                ]
            )

        return self.database.execute(get_item)

    def get_all_items(self) -> List[Item]:
        return self.database.execute(
            lambda conn: [
                Item(id=row[0], name_fr=row[1], type_fr=row[2], level=row[3])
                for row in conn.execute(
                    "SELECT id, name_fr, type_fr, level FROM dofus_items"
                ).fetchall()
            ]
        )
