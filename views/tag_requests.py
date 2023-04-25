import json
import sqlite3
from models import Tag
def get_all_tags():
    """sql get all tags"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.subject
        FROM tags t
        """)
        tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            tag = Tag(row['id'], row['subject'])
            tags.append(tag.__dict__)
        return tags
    
def get_single_tag(tag_id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.subject
        FROM Tags t
        WHERE t.id = ?
        """, (tag_id, ))
        data = db_cursor.fetchone()
        tag = Tag(data['id'], data['subject'])
        return tag.__dict__