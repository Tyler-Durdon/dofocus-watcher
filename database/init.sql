CREATE DATABASE IF NOT EXISTS dofocus_watcher CHARACTER
SET
    utf8mb4 COLLATE utf8mb4_unicode_ci;

USE dofocus_watcher;

DROP TABLE IF EXISTS item_characteristics;
DROP TABLE IF EXISTS item_details;
DROP TABLE IF EXISTS dofus_items;
DROP TABLE IF EXISTS break_results;

-- Table for basic items (French only)
CREATE TABLE dofus_items (
    id INTEGER PRIMARY KEY,
    name_fr TEXT,
    type_fr TEXT,
    level INTEGER
);

-- Table for item details (French, Salar only)
CREATE TABLE item_details (
    id INTEGER PRIMARY KEY,
    name_fr TEXT,
    type_fr TEXT,
    level INTEGER,
    coefficient INTEGER,
    price INTEGER
);

-- Table for item characteristics (linked to item_details)
CREATE TABLE item_characteristics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    name TEXT,
    min_value INTEGER,
    max_value INTEGER,
    FOREIGN KEY (item_id) REFERENCES item_details(id)
);

-- Table for break results
CREATE TABLE break_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    item_name TEXT,
    characteristic TEXT,
    rune_name TEXT,
    runes_generated REAL,
    rune_price REAL,
    best_rune TEXT
);