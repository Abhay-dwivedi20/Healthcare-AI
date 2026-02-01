import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "healthcare.db")

def get_db():
    print("🧠 SQLITE DB PATH:", DB_PATH)  # 🔥 CRITICAL LINE
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
