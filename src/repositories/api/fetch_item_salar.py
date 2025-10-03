import requests
from tabulate import tabulate
from config import DATABASE_PATH, DOFOCUS_API_URL, SERVER_NAME
from database_repository import DatabaseRepository
from items_repository import ItemsRepository
from models.item import Item, Characteristic


def fetch_item_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def extract_french_salar_item(data, server_name, item_id):
    item_name = data["name"]["fr"]
    item_type = data["type"]["name"]["fr"]
    item_level = data["level"]
    characteristics = [
        Characteristic(
            c["name"]["fr"],
            c["from"],
            c["to"]
        )
        for c in data.get("characteristics", [])
    ]
    coefficient = next(
        (c["coefficient"] for c in data.get("coefficients", [])
         if c["serverName"] == server_name),
        None
    )
    price = next(
        (p["price"]
         for p in data.get("prices", []) if p["serverName"] == server_name),
        None
    )
    return Item(
        id=item_id,
        name=item_name,
        type_=item_type,
        level=item_level,
        coefficient=coefficient,
        price=price,
        characteristics=characteristics
    )


def display_ascii_table(item: Item):
    print(f"Nom: {item.name}")
    print(f"Type: {item.type}")
    print(f"Niveau: {item.level}")
    print(f"Coefficient (Salar): {item.coefficient}")
    print(f"Prix (Salar): {item.price}")
    print("\nCaractéristiques:")
    print(tabulate([c.as_dict() for c in item.characteristics],
          headers="keys", tablefmt="grid"))


def main():
    data = fetch_item_data(DOFOCUS_API_URL)
    item_id = 8273
    item = extract_french_salar_item(data, SERVER_NAME, item_id)
    display_ascii_table(item)

    db_repo = DatabaseRepository(DATABASE_PATH)
    db_repo.setup_tables()
    items_repo = ItemsRepository(db_repo)

    items_repo.save_item(item)
    retrieved = items_repo.get_item(item_id)
    if retrieved:
        print("\nItem loaded from DB:")
        display_ascii_table(retrieved)


if __name__ == "__main__":
    main()
