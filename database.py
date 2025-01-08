import sqlite3
import hashlib

# Database setup
DATABASE_NAME = "voting_system.db"

def initialize_database():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE
        )
    """)

    # Create votes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            party TEXT PRIMARY KEY,
            votes INTEGER DEFAULT 0
        )
    """)

    # Initialize parties if not already present
    parties = ["PTI", "MQM", "PMLN", "PPP", "JI"]
    for party in parties:
        cursor.execute("INSERT OR IGNORE INTO votes (party, votes) VALUES (?, 0)", (party,))

    conn.commit()
    conn.close()

def execute_query(query, params=(), fetch=False):
    """Execute a database query and return results if needed."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    conn.commit()
    conn.close()
    return result

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()