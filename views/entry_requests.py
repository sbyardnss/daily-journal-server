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
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])
            entries.append(entry.__dict__)
    return entries


def get_single_entry(id):
    """sql function for getting single entry """
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
        FROM entries e
        WHERE e.id = ?
        """, (id, ))
        data = db_cursor.fetchone()
        entry = Entry(data['id'], data['concept'],
                      data['entry'], data['mood_id'], data['date'])
        return entry.__dict__


def create_entry(new_entry):
    """sql create entry function"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Entries
            (concept, entry, mood_id, date)
        VALUES
            (?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'],))
        id = db_cursor.lastrowid
        new_entry['id'] = id
    return new_entry