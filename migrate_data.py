from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).parent
from src.core.config import DATABASE_PATH

def reset_database(db_path: Path, init_sql_path: Path):
    # remove existing database file
    if db_path.exists():
        print(f"Suppression de la base existante: {db_path}")
        db_path.unlink()
    # ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # read SQL
    if not init_sql_path.exists():
        print(f"Fichier SQL d'initialisation introuvable: {init_sql_path}")
        sys.exit(1)

    sql = init_sql_path.read_text(encoding="utf-8")

    # execute script on new sqlite file
    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(sql)
        conn.commit()
        print(f"Base recreée avec succès: {db_path}")
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'exécution du script SQL: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = Path(DATABASE_PATH)
    init_sql = ROOT / "database" / "init.sql"
    reset_database(db_path, init_sql)
