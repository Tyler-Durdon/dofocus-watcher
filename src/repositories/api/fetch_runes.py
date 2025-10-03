import requests
from config import DATABASE_PATH
from runes_repository import RunesRepository
from models.rune import Rune

DOFOCUS_RUNES_API_URL = "https://dofocus.fr/api/runes?lang=fr"
SERVER_NAME = "Salar"


def print_progress(current, total):
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print(f"\rProgress: |{bar}| {current}/{total}", end='')


def main():
    repo = RunesRepository(DATABASE_PATH)
    repo.setup_table()

    try:
        response = requests.get(DOFOCUS_RUNES_API_URL)
        print(f"\nHTTP Response [{response.status_code}]")
        if not response.ok:
            print(f"HTTP Error: {response.status_code} - {response.reason}")
            return
        data = response.json()
        print(f"Nombre de runes reçues : {len(data)}")
        runes = []
        for idx, rune in enumerate(data, 1):
            name_fr = rune.get("name", {}).get("fr", "")
            characteristic_fr = rune.get(
                "characteristicName", {}).get("fr", "")
            value = rune.get("value")
            weight = rune.get("weight")
            price = None
            date_updated = None
            for price_info in rune.get("latestPrices", []):
                if price_info.get("serverName") == SERVER_NAME:
                    price = price_info.get("price")
                    date_updated = price_info.get("dateUpdated")
                    break
            if price is None:
                continue  # ignorer les runes sans prix sur Salar
            runes.append(Rune(
                id=rune.get("id"),
                name_fr=name_fr,
                characteristic_fr=characteristic_fr,
                value=value,
                weight=weight,
                price=price,
                date_updated=date_updated
            ))
            if idx % 100 == 0 or idx == len(data):
                print_progress(idx, len(data))
        repo.save_runes_batch(runes)
        print("\nSauvegarde terminée.")
    except Exception as e:
        print(f"\nErreur lors de la requête: {e}")


if __name__ == "__main__":
    main()
