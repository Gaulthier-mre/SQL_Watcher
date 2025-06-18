# db_manager.py

import sqlite3

def init_db(db_path):
    """
    Initialise la base de données SQLite avec la table 'alerts' si elle n'existe pas.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            method TEXT NOT NULL,
            uri TEXT NOT NULL,
            date TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def insert_alert(db_path, ip, method, uri, date):
    """
    Insère une alerte dans la base de données SQLite.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (ip, method, uri, date)
        VALUES (?, ?, ?, ?)
    """, (ip, method, uri, date))

    conn.commit()
    conn.close()
