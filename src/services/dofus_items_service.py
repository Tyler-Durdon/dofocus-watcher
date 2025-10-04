from src.repositories.database.dofus_items_repository import DofusItemsRepository
from src.utils.api import make_request
from src.utils.console import print_progress
from src.models.item import Item


class DofusItemsService:
    def __init__(self, database):
        self.database = database
        self.items_repo = DofusItemsRepository(database)

    def fetch_and_save_all_items(self):
        """Récupère et sauvegarde tous les items (FR, sans détails)"""
        print("Récupération des items en cours...")
        try:
            items_data = make_request(
                "GET", "/items?fields=id+name+type+level&lang=fr")
            total = len(items_data or [])
            print(f"Nombre d'items trouvés : {total}")

            items = []
            for idx, item_data in enumerate(items_data or [], 1):
                item = Item.from_api(item_data)
                items.append(item)
                print_progress(idx, total)

            if items:
                self.items_repo.save_items_batch(items)
            print("\nSauvegarde terminée avec succès.")
        except Exception as e:
            print(f"\nErreur lors de la récupération des items: {e}")
