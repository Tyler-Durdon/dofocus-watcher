from src.core.config import DATABASE_PATH
from src.core.database import Database
from src.services.dofus_items_service import DofusItemsService
from src.services.runes_service import RunesService
from src.services.break_calculator_service import BreakCalculatorService
from src.services.items_service import ItemsService
from src.services.bulk_item_details_service import BulkItemDetailsService
from src.utils.console import clear_screen, ConsoleMenu


def main():
    db = Database(str(DATABASE_PATH))
    db.setup_database()
    menu = ConsoleMenu()
    items_service = ItemsService(db)
    bulk_service = BulkItemDetailsService(db)
    while True:
        clear_screen()
        menu.print_header("Dofocus Watcher - Menu Principal")
        menu.print_options([
            "1. Importer tous les items (Salar, FR)",
            "2. Importer toutes les runes (Salar, FR)",
            "3. Récupérer le détail d'un item par id",
            "4. Calculer la rentabilité des brisages",
            "5. Afficher le top 10 des items à briser",
            "6. [CRITIQUE] Récupérer tous les détails d'items (1s delay)",
            "Q. Quitter"
        ])
        choice = menu.get_choice()
        if choice == "1":
            DofusItemsService(db).fetch_and_save_all_items()
            menu.wait_for_user()
        elif choice == "2":
            RunesService(db).fetch_and_save_all_runes()
            menu.wait_for_user()
        elif choice == "3":
            item_id_str = menu.get_input("Entrez l'id de l'item à récupérer: ")
            try:
                item_id = int(item_id_str)
                items_service.fetch_and_save_item_detail(item_id)
            except ValueError:
                print("Id invalide.")
            menu.wait_for_user()
        elif choice == "4":
            BreakCalculatorService(db).calculate_and_display_break_results()
            menu.wait_for_user()
        elif choice == "5":
            BreakCalculatorService(db).display_top_10_profitable_items()
            menu.wait_for_user()
        elif choice == "6":
            bulk_service.fetch_and_save_all_item_details_bulk()
            menu.wait_for_user()
        elif choice.lower() == "q":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")
            menu.wait_for_user()


if __name__ == "__main__":
    main()
