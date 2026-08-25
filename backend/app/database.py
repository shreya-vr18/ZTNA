"""
database.py
Owner: Shreya V R

Sets up the SQLite connection and creates all tables used across the
project (auth, device trust, risk logs). Everyone imports get_db() from
here instead of opening their own sqlite3 connections, so we don't end
up with schema drift between modules.
"""

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent.parent / "db" / "ztna.db"
DB_PATH.parent.mkdir(exist_ok=True)


def get_db():
    """Return a connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't already exist. Safe to call every startup."""
    conn = get_db()
    cur = conn.cursor()

    cur.executescript(
        """
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
        """
    )
    conn.commit()
    conn.close()
