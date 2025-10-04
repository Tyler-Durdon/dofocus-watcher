import time
import requests
from src.repositories.database.items_repository import ItemsRepository
from src.utils.console import print_progress
from src.core.config import DOFOCUS_ITEM_DETAIL_URL, SERVER_NAME, REQUEST_DELAY_SECONDS
from src.models.item import Item, Characteristic


class BulkItemDetailsService:
    def __init__(self, database):
        self.database = database
        self.items_repo = ItemsRepository(database)

    def fetch_and_save_all_item_details_bulk(self):
        """Récupère et sauvegarde les détails de tous les items avec délai et logs"""
        print("Démarrage du fetch CRITIQUE de tous les détails d'items...")
        items = self.items_repo.get_all_items()
        total = len(items)
        print(f"Nombre d'items à traiter : {total}")

        for idx, item in enumerate(items, 1):
            try:
                url = DOFOCUS_ITEM_DETAIL_URL(item.id)
                response = requests.get(url)
                if not response.ok:
                    print(
                        f"Erreur HTTP pour item {item.id}: {response.status_code}")
                    continue
                data = response.json()
                # Récupérer coefficient et sa date pour Salar
                coeff_info = next(
                    (c for c in data.get("coefficients", [])
                     if c.get("serverName") == SERVER_NAME),
                    None
                )
                coefficient = coeff_info.get(
                    "coefficient") if coeff_info else None
                coeff_date = coeff_info.get(
                    "lastUpdate") if coeff_info else None

                # Récupérer prix et sa date pour Salar
                price_info = next(
                    (p for p in data.get("prices", [])
                     if p.get("serverName") == SERVER_NAME),
                    None
                )
                price = price_info.get("price") if price_info else None
                price_date = price_info.get(
                    "lastUpdate") if price_info else None

                characteristics = [
                    Characteristic(
                        name=c.get("name", {}).get("fr", "") or "",
                        min_value=c.get("from", 0) or 0,
                        max_value=c.get("to", 0) or 0
                    )
                    for c in data.get("characteristics", [])
                    if (c.get("name", {}).get("fr", "") or "").lower() != "unknown characteristic"
                ]
                item.coefficient = coefficient
                item.price = price
                item.characteristics = characteristics
                self.items_repo.save_item(item)
                self.items_repo.save_item_details_with_dates(
                    item, coeff_date, price_date)
                print_progress(idx, total)
                print(
                    f"Item {item.id} ({item.name_fr}) sauvegardé. Attente {REQUEST_DELAY_SECONDS}s...")
                time.sleep(REQUEST_DELAY_SECONDS)
            except Exception as e:
                print(f"Erreur sur item {item.id}: {e}")

        print("\nCRITIQUE: Sauvegarde des détails terminée avec succès.")
