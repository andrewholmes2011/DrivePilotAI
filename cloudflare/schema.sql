CREATE TABLE IF NOT EXISTS organization_history (
 id TEXT PRIMARY KEY,
 google_user TEXT NOT NULL,
 created_at TEXT NOT NULL,
 action TEXT NOT NULL,
 source_name TEXT,
 source_id TEXT,
 destination_name TEXT,
 destination_id TEXT,
 details TEXT
);
CREATE INDEX IF NOT EXISTS idx_history_user_created ON organization_history(google_user, created_at DESC);
