import requests
import time
from config import (
    DATABASE_PATH,
    DOFOCUS_ITEMS_API_URL,
    DOFOCUS_ITEM_DETAIL_API_URL,
    SERVER_NAME,
    REQUEST_DELAY_SECONDS
)
from dofus_items_repository import DofusItemsRepository
from item_details_repository import ItemDetailsRepository
from models.dofus_item import DofusItem
from models.item_details import ItemDetails


def print_progress(current, total):
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print(f"\rProgress: |{bar}| {current}/{total}", end='')


def fetch_all_items():
    print("Fetching all items (French only)...")
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
            name_fr = item.get("name", {}).get("fr", "")
            type_fr = item.get("supertype", {}).get("name", {}).get(
                "fr", "") if item.get("supertype") else ""
            items.append(DofusItem(
                id=item.get("id"),
                name_fr=name_fr,
                type_fr=type_fr,
                level=item.get("level")
            ))
            if idx % 100 == 0 or idx == len(data):
                print_progress(idx, len(data))
            time.sleep(REQUEST_DELAY_SECONDS / 10)
        repo.save_items_batch(items)
        print("\nSauvegarde terminée.")
    except Exception as e:
        print(f"\nErreur lors de la requête: {e}")


def fetch_and_save_item_details(item_id):
    print(f"Fetching details for item ID {item_id} (French/Salar only)...")
    repo = ItemDetailsRepository(DATABASE_PATH)
    repo.setup_tables()
    try:
        url = DOFOCUS_ITEM_DETAIL_API_URL.format(id=item_id)
        response = requests.get(url)
        print(f"\nHTTP Response [{response.status_code}]")
        if not response.ok:
            print(f"HTTP Error: {response.status_code} - {response.reason}")
            return
        data = response.json()
        name_fr = data["name"]["fr"]
        type_fr = data["type"]["name"]["fr"]
        level = data["level"]
        characteristics = [
            {
                "Caractéristique": c["name"]["fr"],
                "Min": c["from"],
                "Max": c["to"]
            }
            for c in data.get("characteristics", [])
        ]
        coefficient = next(
            (c["coefficient"] for c in data.get("coefficients", [])
             if c["serverName"] == SERVER_NAME),
            None
        )
        price = next(
            (p["price"] for p in data.get("prices", [])
             if p["serverName"] == SERVER_NAME),
            None
        )
        details = ItemDetails(
            id=item_id,
            name_fr=name_fr,
            type_fr=type_fr,
            level=level,
            coefficient=coefficient,
            price=price,
            characteristics=characteristics
        )
        repo.save_item_details(details)
        print("Sauvegarde terminée.")
    except Exception as e:
        print(f"\nErreur lors de la requête: {e}")


def main_menu():
    while True:
        print("\n--- Menu ---")
        print("1. Saisir un ID pour récupérer et sauvegarder les détails (fr/Salar)")
        print("2. Récupérer et sauvegarder tous les objets (fr)")
        print("0. Quitter")
        choice = input("Votre choix: ")
        if choice == "1":
            item_id = input("Entrez l'ID de l'objet: ")
            if item_id.isdigit():
                fetch_and_save_item_details(int(item_id))
            else:
                print("ID invalide.")
        elif choice == "2":
            fetch_all_items()
        elif choice == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main_menu()
