from database_repository import DatabaseRepository
from models.item import Item, Characteristic


class ItemsRepository:
    def __init__(self, db_repo: DatabaseRepository):
        self.db_repo = db_repo

    def save_item(self, item: Item):
        conn = self.db_repo.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO items (id, name, type, level, coefficient, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item.id,
            item.name,
            item.type,
            item.level,
            item.coefficient,
            item.price
        ))
        cursor.execute(
            "DELETE FROM characteristics WHERE item_id = ?", (item.id,))
        for c in item.characteristics:
            cursor.execute("""
                INSERT INTO characteristics (item_id, name, min_value, max_value)
                VALUES (?, ?, ?, ?)
            """, (
                item.id,
                c.name,
                c.min_value,
                c.max_value
            ))
        conn.commit()
        cursor.close()
        conn.close()

    def get_item(self, item_id):
        conn = self.db_repo.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, type, level, coefficient, price FROM items WHERE id = ?", (item_id,))
        item_row = cursor.fetchone()
        cursor.execute(
            "SELECT name, min_value, max_value FROM characteristics WHERE item_id = ?", (item_id,))
        characteristics = [
            Characteristic(row[0], row[1], row[2])
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        if item_row:
            item = Item(
                id=item_row[0],
                name=item_row[1],
                type_=item_row[2],
                level=item_row[3],
                coefficient=item_row[4],
                price=item_row[5],
                characteristics=characteristics
            )
            return item
        return None
