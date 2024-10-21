import sqlite3
from config import DB_FILE

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        feels_like REAL,
        condition TEXT,
        timestamp INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        avg_temp REAL,
        max_temp REAL,
        min_temp REAL,
        dominant_condition TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        alert_type TEXT,
        value REAL,
        timestamp INTEGER
    )''')

    conn.commit()
    conn.close()
