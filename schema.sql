-- QueerNomads schema: community + city intelligence
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    bio TEXT DEFAULT '',
    pronouns TEXT DEFAULT '',
    home_city TEXT DEFAULT '',
    countries_visited TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    region TEXT NOT NULL,
    summary TEXT NOT NULL,
    queer_nomad_note TEXT NOT NULL,
    cost_level TEXT NOT NULL,
    timezone TEXT DEFAULT '',
    hero_image TEXT DEFAULT '',
    confidence TEXT DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS score_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL,
    description TEXT NOT NULL,
    weight_default REAL NOT NULL DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS city_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER NOT NULL,
    dimension_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK(score BETWEEN 0 AND 100),
    evidence_note TEXT NOT NULL,
    source_count INTEGER NOT NULL DEFAULT 1,
    confidence TEXT NOT NULL DEFAULT 'medium',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (dimension_id) REFERENCES score_dimensions(id),
    UNIQUE(city_id, dimension_id)
);

CREATE TABLE IF NOT EXISTS city_snapshots (
    city_id INTEGER PRIMARY KEY,
    overall_score REAL NOT NULL,
    strengths TEXT NOT NULL,
    tradeoffs TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE TABLE IF NOT EXISTS methodology_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    body TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    city_id INTEGER,
    title TEXT NOT NULL,
    destination TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('nightlife', 'safety', 'community', 'accommodation', 'general')),
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE INDEX IF NOT EXISTS idx_stories_destination ON stories(destination);
CREATE INDEX IF NOT EXISTS idx_stories_category ON stories(category);
CREATE INDEX IF NOT EXISTS idx_stories_user ON stories(user_id);
CREATE INDEX IF NOT EXISTS idx_stories_city ON stories(city_id);
CREATE INDEX IF NOT EXISTS idx_city_scores_city ON city_scores(city_id);
