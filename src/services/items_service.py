import requests

from repositories.database.items_repository import ItemsRepository
from ..utils.api import make_request
from ..utils.console import print_progress
from ..models.item import Item
from ..core.config import DOFOCUS_ITEM_DETAIL_URL, SERVER_NAME
import time


class ItemsService:
    def __init__(self, database):
        self.database = database
        self.items_repo = ItemsRepository(database)

    def fetch_and_save_all_items(self):
        """Récupère et sauvegarde tous les items depuis l'API"""
        print("Récupération des items en cours...")
        try:
            items_data = make_request(
                "GET", "/items?fields=id+name+type+level&lang=fr")
            total = len(items_data or [])
            print(f"Nombre d'items trouvés : {total}")

            for idx, item_data in enumerate(items_data or [], 1):
                # Filtrer et parser uniquement les données françaises
                item = Item.from_api(item_data)
                self._save_item(item)
                print_progress(idx, total)

            print("\nSauvegarde terminée avec succès.")
        except Exception as e:
            print(f"\nErreur lors de la récupération des items: {e}")

    def _save_item(self, item: Item):
        """Persistance élémentaire (dofus_items + details si présents)"""
        self.items_repo.save_item(item)
        if item.characteristics:
            # sauvegarde détaillée si on a des caractéristiques/coefficient/price
            self.items_repo.save_item_details(item)

    def display_item_details(self, item_id: int):
        """Affiche les détails d'un item spécifique"""
        try:
            item = self.items_repo.get_item_by_id(item_id)
            if not item:
                print(f"Item {item_id} non trouvé.")
                return

            print("\n=== Détails de l'item ===")
            print(f"Nom: {item.name_fr}")
            print(f"Type: {item.type_fr}")
            print(f"Niveau: {item.level}")
            print(f"Coefficient: {item.coefficient}")
            print("\nCaractéristiques:")
            for char in item.characteristics:
                print(f"- {char.name}: {char.min_value} à {char.max_value}")

        except Exception as e:
            print(f"Erreur lors de la récupération des détails: {e}")

    def fetch_and_save_all_item_details(self):
        """Récupère et sauvegarde les détails de tous les items (FR/Salar)"""
        print("Récupération des détails de chaque item...")
        items = self.items_repo.get_all_items()
        total = len(items)
        print(f"Nombre d'items à traiter : {total}")

        for idx, item in enumerate(items, 1):
            try:
                url = DOFOCUS_ITEM_DETAIL_URL(item.id)
                import requests
                response = requests.get(url)
                if not response.ok:
                    print(
                        f"Erreur HTTP pour item {item.id}: {response.status_code}")
                    continue
                data = response.json()
                # Récupérer le coefficient et le prix pour Salar
                coefficient = next(
                    (c.get("coefficient") for c in data.get("coefficients", [])
                     if c.get("serverName") == SERVER_NAME),
                    None
                )
                price = next(
                    (p.get("price") for p in data.get("prices", [])
                     if p.get("serverName") == SERVER_NAME),
                    None
                )
                # Récupérer les caractéristiques FR
                characteristics = [
                    Item.characteristics.__dataclass_fields__['name'].type(
                        name=c.get("name", {}).get("fr", "") or "",
                        min_value=c.get("from", 0) or 0,
                        max_value=c.get("to", 0) or 0
                    )
                    for c in data.get("characteristics", [])
                    if (c.get("name", {}).get("fr", "") or "").lower() != "unknown characteristic"
                ]
                # Mettre à jour l'item
                item.coefficient = coefficient
                item.price = price
                item.characteristics = characteristics
                self.save_item_details(item)
                print_progress(idx, total)
                time.sleep(0.1)
            except Exception as e:
                print(f"Erreur sur item {item.id}: {e}")

        print("\nSauvegarde des détails terminée avec succès.")
