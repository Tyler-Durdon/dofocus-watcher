from dataclasses import dataclass
from typing import List, Dict
from src.core.database import Database
from src.models.break_result import BreakResult
from src.repositories.items_repository import ItemsRepository
from src.repositories.runes_repository import RunesRepository
from src.repositories.break_results_repository import BreakResultsRepository

class BreakCalculatorService:
    def __init__(self, database: Database):
        self.database = database
        self.items_repo = ItemsRepository(database)
        self.runes_repo = RunesRepository(database)
        self.results_repo = BreakResultsRepository(database)

    def calculate_and_display_break_results(self):
        """Calcule et affiche la rentabilité des brisages"""
        print("Calcul de la rentabilité en cours...")
        
        items = self.items_repo.get_all_items()
        total = len(items)
        results = []
        
        for idx, item in enumerate(items, 1):
            item_details = self.items_repo.get_item_by_id(item.id)
            if not item_details or not item_details.characteristics:
                continue

            item_results = self._calculate_item_break_value(item_details)
            if item_results:
                results.extend(item_results)
                print(f"Item {idx}/{total}: {item.name_fr} - {len(item_results)} résultats calculés")

        if results:
            self.results_repo.save_results(results)
            print("\nCalculs terminés avec succès.")
            self._display_best_results(results)
        else:
            print("Aucun résultat à afficher.")

    def _calculate_item_break_value(self, item) -> List[BreakResult]:
        """Calcule la valeur de brisage pour un item"""
        if not item.coefficient:
            return []

        results = []
        for char in item.characteristics:
            rune = self.runes_repo.get_rune_by_characteristic(char.name)
            if not rune or not rune.price:
                continue

            avg_value = (char.min_value + char.max_value) / 2
            runes_generated = (avg_value * item.coefficient) / (rune.weight * 100)
            total_value = runes_generated * rune.price

            results.append(BreakResult(
                item_id=item.id,
                item_name=item.name_fr,
                characteristic=char.name,
                rune_name=rune.name_fr,
                runes_generated=runes_generated,
                rune_price=total_value,
                best_rune="pending"  # sera mis à jour plus tard
            ))

        # Marquer la meilleure rune
        if results:
            best_result = max(results, key=lambda x: x.rune_price)
            best_result.best_rune = "yes"

        return results

    def _display_best_results(self, results: List[BreakResult], limit: int = 10):
        """Affiche les meilleurs résultats de brisage"""
        best_results = sorted(
            [r for r in results if r.best_rune == "yes"],
            key=lambda x: x.rune_price,
            reverse=True
        )[:limit]

        print("\nTop 10 des meilleurs items à briser :")
        print("=" * 80)
        print(f"{'Item':<30} {'Caractéristique':<20} {'Rune':<15} {'Valeur':<10}")
        print("-" * 80)

        for result in best_results:
            print(f"{result.item_name[:30]:<30} "
                  f"{result.characteristic[:20]:<20} "
                  f"{result.rune_name[:15]:<15} "
                  f"{int(result.rune_price):>8,} k")

    def display_top_10_profitable_items(self, limit: int = 10):
        """Affiche le top N des résultats stockés"""
        best_results = self.results_repo.get_top_results(limit)
        if not best_results:
            print("Aucun résultat enregistré pour l'instant.")
            return

        print("\nTop {} des meilleurs items à briser :".format(limit))
        print("=" * 80)
        print(f"{'Item':<30} {'Caractéristique':<20} {'Rune':<15} {'Valeur':<10}")
        print("-" * 80)

        for result in best_results:
            # rune_price peut être None; sécuriser l'affichage
            value_display = int(result.rune_price) if result.rune_price else 0
            print(f"{result.item_name[:30]:<30} "
                  f"{result.characteristic[:20]:<20} "
                  f"{result.rune_name[:15]:<15} "
                  f"{value_display:>8,} k")
