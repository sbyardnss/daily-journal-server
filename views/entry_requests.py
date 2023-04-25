import json
import sqlite3
from models import Entry, Mood, Entry_tag
from .tag_requests import get_single_tag


def get_all_entries():
    """sql friendly get all entries function"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT DISTINCT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label,
            (
            SELECT GROUP_CONCAT(t.id)
            FROM Entry_tags et JOIN tags t ON et.tag_id = t.id
            WHERE et.entry_id = e.id
            ) as entry_tags
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        LEFT OUTER JOIN entry_tags et ON e.id = et.entry_id
        LEFT OUTER JOIN TAGS t ON t.id = et.tag_id
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])
            mood = Mood(row['mood_id'], row['label'])
            entry.mood = mood.__dict__
            entry_tags = row['entry_tags'].split(',') if row['entry_tags'] else []
            entry_tags_arr = []
            for tag_id in entry_tags:
                tag_object = get_single_tag(tag_id)
                entry_tags_arr.append(tag_object)
            entry.entry_tags = entry_tags_arr
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


def search_entries(terms):
    """sql function for returning entry search"""
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
        WHERE e.entry LIKE ?
        """, (f'%{terms}%', ))
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])
            entries.append(entry.__dict__)
    return entries


def create_entry(new_entry):
    """sql create entry function"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT *
            FROM Entries e
            LEFT OUTER JOIN Entry_tags et
                on e.id = et.entry_id
            LEFT OUTER JOIN TAGS t
                on t.id = et.tag_id
        """)
        db_cursor.execute("""
        INSERT INTO Entries
            (concept, entry, mood_id, date)
        VALUES
            (?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'],))
        id = db_cursor.lastrowid
        new_entry['id'] = id
        # loop below is looking for list property on entries
        # that contains ONLY corresponding tag ids. not objects
        for tag in new_entry['entry_tags']:
            db_cursor.execute("""
            INSERT INTO Entry_tags
                (entry_id, tag_id)
            VALUES
                (?, ?)
            """, (new_entry['id'], tag,))
        return new_entry

def update_entry(id, new_entry):
    """sql update entry function"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
            WHERE id = ?;
            """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], id))
    rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    return True

def delete_entry(id):
    """sql delete entry function"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Entries
        WHERE id = ?
        """, (id, ))
