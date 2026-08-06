import sqlite3
from passlib.context import CryptContext

# Set up the password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("password123")

# SQLite will create this file in your main project folder
DB_PATH = "ztna.db"

try:
    # Connect to the local SQLite file
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE, 
            password_hash TEXT
        );
    """)

    # Create the devices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, 
            device_hash TEXT, 
            browser TEXT, 
            os TEXT, 
            ip TEXT
        );
    """)

    # Insert a dummy user
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("testuser", hashed_password)
        )
        print("✅ SQLite database created and 'testuser' inserted successfully!")
    except sqlite3.IntegrityError:
        print("✅ SQLite database exists and 'testuser' is already in it.")

    # Save changes and close
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Error setting up SQLite database: {e}")