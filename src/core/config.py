from pathlib import Path

# Chemins
ROOT_DIR = Path(__file__).parent.parent.parent
DATABASE_PATH = ROOT_DIR / "data" / "dofocus_watcher.db"

# API
DOFOCUS_API_BASE_URL = "https://dofocus.fr/api"
DOFOCUS_ITEMS_API_URL = f"{DOFOCUS_API_BASE_URL}/items?fields=id+name+type+level&lang=fr"
DOFOCUS_RUNES_API_URL = f"{DOFOCUS_API_BASE_URL}/runes?lang=fr"
DOFOCUS_ITEM_DETAIL_URL = lambda item_id: f"{DOFOCUS_API_BASE_URL}/items/{item_id}?lang=fr"

# Champs à récupérer pour les items
ITEMS_FIELDS = "id+name+type+level"

# Configuration serveur
SERVER_NAME = "Salar"
REQUEST_DELAY_SECONDS = 1
