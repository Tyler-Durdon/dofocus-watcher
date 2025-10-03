import sqlite3
from config import DATABASE_PATH
from break_results_repository import BreakResultsRepository
from models.break_result import BreakResult


def fetch_all_items(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name_fr, type_fr, level FROM dofus_items")
    items = cursor.fetchall()
    cursor.close()
    return items


def fetch_item_details(conn, item_id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT coefficient FROM item_details WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def fetch_characteristics(conn, item_id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, min_value, max_value FROM item_characteristics WHERE item_id = ?", (item_id,))
    characteristics = cursor.fetchall()
    cursor.close()
    return characteristics


def fetch_rune(conn, characteristic_name):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT value, weight, price FROM runes
        WHERE name_fr = ? OR characteristic_fr = ?
        AND price IS NOT NULL
        ORDER BY weight DESC LIMIT 1
    """, (characteristic_name, characteristic_name))
    row = cursor.fetchone()
    cursor.close()
    return row if row else None


def calculate_runes_and_price(item_id, item_name, coefficient, characteristics, conn):
    total_runes = 0.0
    total_price = 0.0
    details = []
    for char_name, min_val, max_val in characteristics:
        char_value = (min_val + max_val) / 2  # average value
        rune_data = fetch_rune(conn, char_name)
        if rune_data:
            rune_value, rune_weight, rune_price = rune_data
            if rune_weight and coefficient:
                num_runes = (char_value * coefficient) / rune_weight
                price = num_runes * rune_price
                details.append({
                    "caractéristique": char_name,
                    "nombre_runes": num_runes,
                    "prix_total": price
                })
                total_runes += num_runes
                total_price += price
    return total_runes, total_price, details


def main():
    conn = sqlite3.connect(DATABASE_PATH)
    items = fetch_all_items(conn)
    print(f"Nombre d'items trouvés : {len(items)}")
    results = []
    repo = BreakResultsRepository(DATABASE_PATH)
    repo.setup_table()
    for item_id, name_fr, type_fr, level in items:
        coefficient = fetch_item_details(conn, item_id)
        characteristics = fetch_characteristics(conn, item_id)
        if coefficient is not None and characteristics:
            rune_details = []
            best_rune = None
            best_price = 0
            for char_name, min_val, max_val in characteristics:
                char_value = (min_val + max_val) / 2
                rune_data = fetch_rune(conn, char_name)
                if rune_data:
                    rune_value, rune_weight, rune_price = rune_data
                    if rune_weight and coefficient:
                        num_runes = (char_value * coefficient) / rune_weight
                        price = num_runes * rune_price
                        rune_details.append(
                            (char_name, rune_value, num_runes, price))
                        if price > best_price:
                            best_price = price
                            best_rune = rune_value
            for char_name, rune_name, num_runes, price in rune_details:
                result = BreakResult(
                    item_id=item_id,
                    item_name=name_fr,
                    characteristic=char_name,
                    rune_name=rune_name,
                    runes_generated=num_runes,
                    rune_price=price,
                    best_rune="yes" if rune_name == best_rune else ""
                )
                results.append(result)
            print(
                f"{name_fr} (ID {item_id}) : {len(rune_details)} caractéristiques traitées")
    repo.save_results_batch(results)
    conn.close()
    print("\nCalcul et sauvegarde des résultats terminés.")


if __name__ == "__main__":
    main()
