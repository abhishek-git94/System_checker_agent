 
# utils/storage.py

import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "symptom_history.db"

def init_db():
    """Database banao agar exist nahi karti"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptom_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            symptoms TEXT,
            severity TEXT,
            diagnosis TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_symptom(user_id: str, symptoms: str, severity: str, diagnosis: str):
    """Symptom history save karo"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO symptom_history (user_id, symptoms, severity, diagnosis)
        VALUES (?, ?, ?, ?)
    """, (user_id, symptoms, severity, diagnosis))
    conn.commit()
    conn.close()

def get_history(user_id: str):
    """User ki purani history lo"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM symptom_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10",
        conn,
        params=(user_id,)
    )
    conn.close()
    return df

def get_patterns(user_id: str):
    """Recurring symptoms dhundo"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT symptoms, COUNT(*) as count FROM symptom_history WHERE user_id = ? GROUP BY symptoms ORDER BY count DESC",
        conn,
        params=(user_id,)
    )
    conn.close()
    return df