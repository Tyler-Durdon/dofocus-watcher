from typing import List, Optional
from src.core.database import Database
from src.models.rune import Rune


class RunesRepository:
    def __init__(self, database: Database):
        self.database = database

    def save_rune(self, rune: Rune) -> None:
        self.database.execute(lambda conn: conn.execute("""
            INSERT OR REPLACE INTO runes 
            (id, name_fr, characteristic_fr, value, weight, price, date_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rune.as_tuple()))

    def save_runes_batch(self, runes: List[Rune]) -> None:
        self.database.execute(
            lambda conn: conn.executemany("""
                INSERT OR REPLACE INTO runes 
                (id, name_fr, characteristic_fr, value, weight, price, date_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [rune.as_tuple() for rune in runes])
        )

    def get_all_runes(self) -> List[Rune]:
        return self.database.execute(
            lambda conn: [
                Rune(*row) for row in conn.execute(
                    "SELECT id, name_fr, characteristic_fr, value, weight, price, date_updated FROM runes"
                ).fetchall()
            ]
        )

    def get_rune_by_characteristic(self, characteristic: str) -> Optional[Rune]:
        def get_rune(conn):
            # Parenthèse pour forcer la priorité entre OR et AND
            row = conn.execute("""
                SELECT id, name_fr, characteristic_fr, value, weight, price, date_updated FROM runes 
                WHERE (characteristic_fr = ? OR name_fr = ?)
                AND price IS NOT NULL
                ORDER BY weight DESC LIMIT 1
            """, (characteristic, characteristic)).fetchone()
            return Rune(*row) if row else None

        return self.database.execute(get_rune)
