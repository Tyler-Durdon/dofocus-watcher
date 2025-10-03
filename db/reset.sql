-- RESET / CREATE schema for Dofocus watcher (PostgreSQL)

-- WARNING: This will DROP existing tables in the schema public that are named below.
BEGIN;

-- Drop existing tables (if any)
DROP TABLE IF EXISTS focus_results CASCADE;
DROP TABLE IF EXISTS price_history CASCADE;
DROP TABLE IF EXISTS item_prices CASCADE;
DROP TABLE IF EXISTS item_details CASCADE;
DROP TABLE IF EXISTS item_runes CASCADE;
DROP TABLE IF EXISTS runes CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS servers CASCADE;
DROP TABLE IF EXISTS audits CASCADE;

-- Servers (e.g., Salar)
CREATE TABLE servers (
    id              BIGSERIAL PRIMARY KEY,
    code            TEXT NOT NULL UNIQUE,      -- e.g. 'salar'
    name            TEXT NOT NULL,             -- e.g. 'Salar'
    region          TEXT,                      -- optional
    language        TEXT DEFAULT 'fr',         -- default 'fr'
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Static items table (one row per item id on DoFocus)
CREATE TABLE items (
    id              BIGSERIAL PRIMARY KEY,
    external_id     TEXT NOT NULL UNIQUE,      -- identifier from DoFocus API
    name            TEXT NOT NULL,
    level           INTEGER,
    type            TEXT,                       -- e.g., 'armure', 'anneau', ...
    rarity          TEXT,
    server_id       BIGINT REFERENCES servers(id) ON DELETE SET NULL,
    source_url      TEXT,
    tags            TEXT[],                     -- categories, localization hints
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_items_external_id ON items(external_id);
CREATE INDEX idx_items_server_id ON items(server_id);

-- Runes (distinct rune definitions)
CREATE TABLE runes (
    id              BIGSERIAL PRIMARY KEY,
    external_id     TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    rarity          TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Item <-> Rune relationships (if breaking an item yields runes)
CREATE TABLE item_runes (
    id              BIGSERIAL PRIMARY KEY,
    item_id         BIGINT REFERENCES items(id) ON DELETE CASCADE,
    rune_id         BIGINT REFERENCES runes(id) ON DELETE CASCADE,
    min_qty         INTEGER DEFAULT 0,
    max_qty         INTEGER DEFAULT 0,
    chance_percent  NUMERIC(5,2) DEFAULT 0,    -- probability (0-100)
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now(),
    UNIQUE(item_id, rune_id)
);

CREATE INDEX idx_item_runes_item ON item_runes(item_id);

-- Item details / characteristics (flexible JSONB to store base stats)
CREATE TABLE item_details (
    id              BIGSERIAL PRIMARY KEY,
    item_id         BIGINT REFERENCES items(id) ON DELETE CASCADE,
    server_id       BIGINT REFERENCES servers(id) ON DELETE SET NULL,
    details_json    JSONB,                     -- raw scraped attributes (FR)
    extracted_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
    source_url      TEXT
);

CREATE INDEX idx_item_details_item_server ON item_details(item_id, server_id);

-- Current item prices (latest snapshot per server)
CREATE TABLE item_prices (
    id              BIGSERIAL PRIMARY KEY,
    item_id         BIGINT REFERENCES items(id) ON DELETE CASCADE,
    server_id       BIGINT REFERENCES servers(id) ON DELETE SET NULL,
    price           NUMERIC(18,4) NOT NULL,    -- price in kamas
    currency        TEXT DEFAULT 'kamas',
    quality         TEXT,                      -- if applicable
    last_checked    TIMESTAMP WITH TIME ZONE DEFAULT now(),
    source_url      TEXT,
    UNIQUE(item_id, server_id)
);

CREATE INDEX idx_item_prices_item_server ON item_prices(item_id, server_id);

-- Historical prices (time series)
CREATE TABLE price_history (
    id              BIGSERIAL PRIMARY KEY,
    item_id         BIGINT REFERENCES items(id) ON DELETE CASCADE,
    server_id       BIGINT REFERENCES servers(id) ON DELETE SET NULL,
    price           NUMERIC(18,4) NOT NULL,
    observed_at     TIMESTAMP WITH TIME ZONE DEFAULT now(),
    source_url      TEXT,
    source_meta     JSONB
);

CREATE INDEX idx_price_history_item_time ON price_history(item_id, observed_at DESC);

-- Cached focus calculation results
CREATE TABLE focus_results (
    id                  BIGSERIAL PRIMARY KEY,
    item_id             BIGINT REFERENCES items(id) ON DELETE CASCADE,
    server_id           BIGINT REFERENCES servers(id) ON DELETE SET NULL,
    calculated_at       TIMESTAMP WITH TIME ZONE DEFAULT now(),
    focus_used          BOOLEAN DEFAULT FALSE,
    strategy            TEXT,            -- 'optimal', 'no_focus', 'with_focus', etc.
    expected_value      NUMERIC(20,6),   -- estimated kamas value after breaking
    expected_runes_json JSONB,           -- details per rune {rune_id: {avg_qty, price, value}}
    params_json         JSONB,           -- parameters used for calc (drop rates, focus cost, etc)
    UNIQUE(item_id, server_id, strategy)
);

CREATE INDEX idx_focus_item_server ON focus_results(item_id, server_id);

-- Audits / scrape logs
CREATE TABLE audits (
    id              BIGSERIAL PRIMARY KEY,
    action          TEXT NOT NULL,        -- e.g., 'scrape_item', 'scrape_price'
    server_id       BIGINT REFERENCES servers(id) ON DELETE SET NULL,
    item_external_id TEXT,
    status          TEXT,                 -- 'ok', 'error'
    message         TEXT,
    meta            JSONB,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_audits_action_time ON audits(action, created_at DESC);

-- Example constraints or helper tables could be added later (users, api_keys, jobs, etc)

COMMIT;

-- Optional: example server row for Salar
INSERT INTO servers (code, name, language, region)
VALUES ('salar','Salar','fr','EU')
ON CONFLICT (code) DO NOTHING;
