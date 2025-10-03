from src.core.config import DATABASE_PATH
from src.core.database import Database
from src.services.items_service import ItemsService
from src.services.runes_service import RunesService
from src.services.break_calculator_service import BreakCalculatorService
from src.utils.console import ConsoleMenu, clear_screen


def setup_services():
    """Initialise les services nécessaires"""
    database = Database(DATABASE_PATH)
    database.setup_database()

    return {
        'items': ItemsService(database),
        'runes': RunesService(database),
        'calculator': BreakCalculatorService(database)
    }


def main():
    services = setup_services()
    menu = ConsoleMenu()

    while True:
        clear_screen()
        menu.print_header("DofocusWatcher - Menu Principal")
        menu.print_options([
            "1. Récupérer tous les items (liste simple)",
            "2. Récupérer toutes les runes",
            "3. Récupérer et sauvegarder les détails de tous les items",
            "4. Consulter le détail d'un item",
            "5. Calculer la rentabilité des brisages",
            "6. Top 10 des objets les plus rentables",
            "0. Quitter"
        ])

        choice = menu.get_choice("Votre choix: ")

        try:
            if choice == "1":
                services['items'].fetch_and_save_all_items()
            elif choice == "2":
                services['runes'].fetch_and_save_all_runes()
            elif choice == "3":
                services['items'].fetch_and_save_all_item_details()
            elif choice == "4":
                item_id = menu.get_input("Entrez l'ID de l'item: ")
                if item_id.isdigit():
                    services['items'].display_item_details(int(item_id))
                else:
                    print("ID invalide.")
            elif choice == "5":
                services['calculator'].calculate_and_display_break_results()
            elif choice == "6":
                services['calculator'].display_top_10_profitable_items()
            elif choice == "0":
                print("Au revoir!")
                break
            else:
                print("Choix invalide")
        except Exception as e:
            print(f"Erreur: {e}")

        menu.wait_for_user()


if __name__ == "__main__":
    main()
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
            if c["name"]["fr"].lower() != "unknown characteristic"
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
        repr.save_item_details(details)
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
