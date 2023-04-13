import json
import sqlite3
from models import Entry

def get_all_entries():
    """sql friendly get all entries function"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Entries e
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])
            entries.append(entry.__dict__)
    return entries