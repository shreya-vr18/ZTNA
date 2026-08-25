-- ============================
-- ZTNA Database Schema
-- ============================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    failed_login_count INTEGER DEFAULT 0,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    device_hash TEXT NOT NULL,
    browser TEXT,
    os TEXT,
    ip_address TEXT,
    trust_score REAL DEFAULT 0.0,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    device_id INTEGER REFERENCES devices(id),
    token TEXT NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource TEXT NOT NULL,
    min_trust_score REAL NOT NULL,
    allowed_roles TEXT
);

CREATE TABLE IF NOT EXISTS risk_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    session_id TEXT,
    identity_risk REAL,
    device_risk REAL,
    final_risk REAL,
    decision TEXT,
    reason TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================
-- Seed data (sample policies)
-- ============================
INSERT OR IGNORE INTO policies (id, resource, min_trust_score, allowed_roles)
VALUES
    (1, '/broker/evaluate', 0.5, 'user,admin'),
    (2, '/admin/dashboard', 0.8, 'admin'),
    (3, '/reports/export', 0.6, 'user,admin');
