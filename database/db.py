"""
SQLite database module for storing user assessments and risk results.
Lightweight storage for research data and audit trail.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_PATH


def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            condition_type TEXT NOT NULL,
            user_inputs TEXT,
            risk_probability REAL,
            risk_level TEXT,
            model_used TEXT DEFAULT 'ensemble'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            demographics TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def save_assessment(condition_type: str, user_inputs: dict, risk_probability: float, risk_level: str):
    """Save a risk assessment to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO assessments (condition_type, user_inputs, risk_probability, risk_level)
        VALUES (?, ?, ?, ?)
    """, (condition_type, json.dumps(user_inputs), risk_probability, risk_level))
    
    conn.commit()
    conn.close()


def get_assessment_stats():
    """Get summary statistics for research reporting."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT condition_type, COUNT(*) as count, 
               AVG(risk_probability) as avg_risk
        FROM assessments
        GROUP BY condition_type
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_all_assessments():
    """Get all assessments for the admin dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assessments ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
