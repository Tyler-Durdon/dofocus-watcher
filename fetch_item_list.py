import requests
import time
from config import (
    DATABASE_PATH,
    DOFUSDB_ITEMS_API_URL,
    REQUEST_DELAY_SECONDS,
    MAX_REQUESTS
)
from dofocus_items_repository import DofocusItemsRepository
from models.dofocus_item import DofocusItem


def print_progress(current, total):
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print(f"\rProgress: |{bar}| {current}/{total} requests", end='')


def extract_item_model(item):
    # Extract names and types in all languages if available
    name_fr = item.get("name", {}).get("fr", "")
    name_en = item.get("name", {}).get("en", "")
    name_es = item.get("name", {}).get("es", "")
    type_fr = item.get("type", {}).get("name", {}).get(
        "fr", "") if item.get("type") else ""
    type_en = item.get("type", {}).get("name", {}).get(
        "en", "") if item.get("type") else ""
    type_es = item.get("type", {}).get("name", {}).get(
        "es", "") if item.get("type") else ""
    return DofocusItem(
        id=item.get("id"),
        name_fr=name_fr,
        name_en=name_en,
        name_es=name_es,
        type_fr=type_fr,
        type_en=type_en,
        type_es=type_es,
        level=item.get("level"),
        price=item.get("price"),
        img=item.get("img")
    )


def main():
    repo = DofocusItemsRepository(DATABASE_PATH)
    repo.setup_table()

    total_requests = 0
    skip = 0
    limit = 10  # API default, can be changed if needed

    while total_requests < MAX_REQUESTS:
        try:
            params = {"limit": limit, "skip": skip}
            response = requests.get(DOFUSDB_ITEMS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get("data", [])
            for item in items:
                item_model = extract_item_model(item)
                repo.save_item(item_model)
            total_requests += 1
            print_progress(total_requests, MAX_REQUESTS)
            skip += limit
            time.sleep(REQUEST_DELAY_SECONDS)
        except Exception as e:
            print(f"\nError on request {total_requests + 1}: {e}")
            break

    print("\nDone.")


if __name__ == "__main__":
    main()
