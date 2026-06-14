import os
import sqlite3
from datetime import datetime

def init_db():
    os.makedirs('db', exist_ok=True)
    conn = sqlite3.connect('db/memory.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, student_id TEXT, role TEXT, message TEXT, timestamp TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS student_profile (student_id TEXT PRIMARY KEY, location TEXT, housing_type TEXT, last_updated TEXT)''')
    conn.commit()
    conn.close()

def save_message(student_id, role, message):
    conn = sqlite3.connect('db/memory.db')
    conn.execute('INSERT INTO conversations VALUES (NULL,?,?,?,?)', (student_id, role, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history(student_id, limit=10):
    conn = sqlite3.connect('db/memory.db')
    rows = conn.execute('SELECT role, message FROM conversations WHERE student_id=? ORDER BY id DESC LIMIT ?', (student_id, limit)).fetchall()
    conn.close()
    return list(reversed(rows))

def save_profile(student_id, location, housing_type):
    conn = sqlite3.connect('db/memory.db')
    conn.execute('''INSERT INTO student_profile VALUES (?,?,?,?) ON CONFLICT(student_id) DO UPDATE SET location=excluded.location, housing_type=excluded.housing_type, last_updated=excluded.last_updated''', (student_id, location, housing_type, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_profile(student_id):
    conn = sqlite3.connect('db/memory.db')
    row = conn.execute('SELECT location, housing_type FROM student_profile WHERE student_id=?', (student_id,)).fetchone()
    conn.close()
    return {'location': row[0], 'housing_type': row[1]} if row else {}
