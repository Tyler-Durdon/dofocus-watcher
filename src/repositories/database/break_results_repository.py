from typing import List
from src.core.database import Database
from src.models.break_result import BreakResult


class BreakResultsRepository:
    def __init__(self, database: Database):
        self.database = database

    def save_results(self, results: List[BreakResult]) -> None:
        self.database.execute(
            lambda conn: conn.executemany("""
                INSERT INTO break_results (
                    item_id, item_name, characteristic, 
                    rune_name, runes_generated, rune_price, best_rune
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [result.as_tuple() for result in results])
        )

    def get_results_by_item(self, item_id: int) -> List[BreakResult]:
        return self.database.execute(
            lambda conn: [
                BreakResult(*row) for row in conn.execute("""
                    SELECT item_id, item_name, characteristic, rune_name, runes_generated, rune_price, best_rune 
                    FROM break_results 
                    WHERE item_id = ?
                    ORDER BY rune_price DESC
                """, (item_id,)).fetchall()
            ]
        )

    def get_top_results(self, limit: int = 10) -> List[BreakResult]:
        """Récupère les meilleurs résultats globalement (par valeur)"""
        return self.database.execute(
            lambda conn: [
                BreakResult(*row) for row in conn.execute("""
                    SELECT item_id, item_name, characteristic, rune_name, runes_generated, rune_price, best_rune
                    FROM break_results
                    ORDER BY rune_price DESC
                    LIMIT ?
                """, (limit,)).fetchall()
            ]
        )
