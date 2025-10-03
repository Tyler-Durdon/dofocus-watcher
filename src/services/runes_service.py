from repositories.database.runes_repository import RunesRepository
from ..utils.api import make_request
from ..utils.console import print_progress
from ..models.rune import Rune
from ..core.config import SERVER_NAME


class RunesService:
    def __init__(self, database):
        self.database = database
        self.runes_repo = RunesRepository(database)

    def fetch_and_save_all_runes(self):
        """Récupère et sauvegarde toutes les runes depuis l'API"""
        print("Récupération des runes en cours...")
        try:
            runes_data = make_request("GET", "/runes?lang=fr")
            total = len(runes_data or [])
            print(f"Nombre de runes trouvées : {total}")

            runes = []
            for idx, rune_data in enumerate(runes_data or [], 1):
                # Filtrer sur le serveur Salar
                price_info = next(
                    (p for p in rune_data.get("latestPrices", [])
                     if p.get("serverName") == SERVER_NAME),
                    None
                )
                if not price_info:
                    continue
                rune = Rune.from_api(rune_data)
                runes.append(rune)
                print_progress(idx, total)

            if runes:
                self.runes_repo.save_runes_batch(runes)
            print("\nSauvegarde terminée avec succès.")
        except Exception as e:
            print(f"\nErreur lors de la récupération des runes: {e}")
