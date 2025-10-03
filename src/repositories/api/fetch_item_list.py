import requests
import time
from config import DATABASE_PATH, REQUEST_DELAY_SECONDS
from dofus_items_repository import DofusItemsRepository
from models.dofus_item import DofusItem

DOFOCUS_ITEMS_API_URL = "https://dofocus.fr/api/items?fields=id+name+supertype.id+level&lang=fr"


def print_progress(current, total):
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print(f"\rProgress: |{bar}| {current}/{total}", end='')


def extract_item_model(item):
    name_fr = item.get("name", {}).get("fr", "")
    type_fr = item.get("supertype", {}).get("name", {}).get(
        "fr", "") if item.get("supertype") else ""
    return DofusItem(
        id=item.get("id"),
        name_fr=name_fr,
        type_fr=type_fr,
        level=item.get("level")
    )


def main():
    repo = DofusItemsRepository(DATABASE_PATH)
    repo.setup_table()

    try:
        response = requests.get(DOFOCUS_ITEMS_API_URL)
        print(f"\nHTTP Response [{response.status_code}]")
        if not response.ok:
            print(f"HTTP Error: {response.status_code} - {response.reason}")
            return
        data = response.json()
        if not isinstance(data, list):
            print(f"Error: Unexpected response format: {data}")
            return
        print(f"Nombre d'objets reçus : {len(data)}")
        items = []
        for idx, item in enumerate(data, 1):
            try:
                item_model = extract_item_model(item)
                items.append(item_model)
                if idx % 100 == 0 or idx == len(data):
                    print_progress(idx, len(data))
            except Exception as save_err:
                print(
                    f"Erreur lors du traitement de l'objet {item.get('id')}: {save_err}")
            time.sleep(REQUEST_DELAY_SECONDS / 10)
        repo.save_items_batch(items)
        print("\nSauvegarde terminée.")
    except Exception as e:
        print(f"\nErreur lors de la requête: {e}")


if __name__ == "__main__":
    main()
