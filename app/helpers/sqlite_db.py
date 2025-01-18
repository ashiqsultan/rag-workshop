import sqlite3
from contextlib import contextmanager
from app.notes.schema import Note, Notes


DB_PATH = "notes.db"


def init_db():
    """Initialize the database and create tables if they don't exist"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Create notes table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()


@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def save_note(note_id: str, content: str) -> bool:
    """Save a note to the database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (id, content) VALUES (?, ?)", (note_id, content)
        )
        conn.commit()
    return True


def get_by_id(note_id: str) -> Note:
    """Retrieve a note by its ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, created_at FROM notes WHERE id = ?", (note_id,)
        )
        result = cursor.fetchone()
        if result:
            return Note(id=result[0], content=result[1], created_at=result[2])
        return None


def get_all() -> Notes:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM notes")
        notes = cursor.fetchall()
        return Notes(notes=[Note(id=note[0], content=note[1]) for note in notes])
