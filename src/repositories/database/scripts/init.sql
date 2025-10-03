PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

-- Drop tables if exist (order agnostique)
DROP TABLE IF EXISTS focus_results;
DROP TABLE IF EXISTS price_history;
DROP TABLE IF EXISTS item_prices;
DROP TABLE IF EXISTS item_runes;
DROP TABLE IF EXISTS item_characteristics;
DROP TABLE IF EXISTS item_details;
DROP TABLE IF EXISTS dofus_items;
DROP TABLE IF EXISTS break_results;
DROP TABLE IF EXISTS runes;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS servers;
DROP TABLE IF EXISTS audits;

-- Servers (example)
CREATE TABLE servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    region TEXT,
    language TEXT DEFAULT 'fr',
    created_at TEXT DEFAULT (datetime('now'))
);

-- Basic items table (static list)
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_id TEXT UNIQUE,
    name TEXT NOT NULL,
    level INTEGER,
    type TEXT,
    rarity TEXT,
    server_id INTEGER,
    source_url TEXT,
    tags TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(server_id) REFERENCES servers(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_items_external_id ON items(external_id);
CREATE INDEX IF NOT EXISTS idx_items_server_id ON items(server_id);

-- Runes
CREATE TABLE runes (
    id INTEGER PRIMARY KEY,
    name_fr TEXT,
    characteristic_fr TEXT,
    value INTEGER,
    weight INTEGER,
    price REAL,
    date_updated TEXT
);

-- Item <-> rune mapping (if applicable)
CREATE TABLE item_runes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    rune_id INTEGER,
    min_qty INTEGER DEFAULT 0,
    max_qty INTEGER DEFAULT 0,
    chance_percent REAL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(item_id, rune_id),
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY(rune_id) REFERENCES runes(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_item_runes_item ON item_runes(item_id);

-- Table for basic items (legacy compatibility)
CREATE TABLE dofus_items (
    id INTEGER PRIMARY KEY,
    name_fr TEXT,
    type_fr TEXT,
    level INTEGER
);

-- Detailed item info (Salar, FR)
CREATE TABLE item_details (
    id INTEGER PRIMARY KEY,
    name_fr TEXT,
    type_fr TEXT,
    level INTEGER,
    coefficient REAL,
    price REAL,
    updated_at TEXT
);

-- Item characteristics linked to details
CREATE TABLE item_characteristics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    name TEXT,
    min_value INTEGER,
    max_value INTEGER,
    FOREIGN KEY (item_id) REFERENCES item_details(id) ON DELETE CASCADE
);

-- Current item prices snapshot
CREATE TABLE item_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    server_id INTEGER,
    price REAL NOT NULL,
    currency TEXT DEFAULT 'kamas',
    quality TEXT,
    last_checked TEXT DEFAULT (datetime('now')),
    source_url TEXT,
    UNIQUE(item_id, server_id),
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY(server_id) REFERENCES servers(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_item_prices_item_server ON item_prices(item_id, server_id);

-- Historical prices
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    server_id INTEGER,
    price REAL NOT NULL,
    observed_at TEXT DEFAULT (datetime('now')),
    source_url TEXT,
    source_meta TEXT,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY(server_id) REFERENCES servers(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_price_history_item_time ON price_history(item_id, observed_at DESC);

-- Break results cache / stored computations
CREATE TABLE break_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    item_name TEXT,
    characteristic TEXT,
    rune_name TEXT,
    runes_generated REAL,
    rune_price REAL,
    best_rune TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- Focus calculation results (cached)
CREATE TABLE focus_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    server_id INTEGER,
    calculated_at TEXT DEFAULT (datetime('now')),
    focus_used INTEGER DEFAULT 0,
    strategy TEXT,
    expected_value REAL,
    expected_runes_json TEXT,
    params_json TEXT,
    UNIQUE(item_id, server_id, strategy),
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY(server_id) REFERENCES servers(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_focus_item_server ON focus_results(item_id, server_id);

-- Audits / logs
CREATE TABLE audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    server_id INTEGER,
    item_external_id TEXT,
    status TEXT,
    message TEXT,
    meta TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(server_id) REFERENCES servers(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_audits_action_time ON audits(action, created_at DESC);

COMMIT;
PRAGMA foreign_keys = ON;

-- Insert example server Salar (no-op if exists)
INSERT OR IGNORE INTO servers (code, name, language, region)
VALUES ('salar', 'Salar', 'fr', 'EU');