import json
import sqlite3
from models import Mood

def get_all_moods():
    """sql get all entries function"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """)
        moods = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)
    return moods