import aiosqlite
from datetime import date

DB_PATH = 'mood.db'

CREATE_EVENTS_TABLE = '''
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_date TEXT,
    description TEXT,
    emotion TEXT,
    rating INTEGER
)'''

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_EVENTS_TABLE)
        await db.commit()

async def add_event(user_id: int, event_date: str, description: str, emotion: str, rating: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            'INSERT INTO events(user_id, event_date, description, emotion, rating) VALUES (?,?,?,?,?)',
            (user_id, event_date, description, emotion, rating)
        )
        await db.commit()

async def update_event(user_id: int, event_date: str, description: str, emotion: str, rating: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            'UPDATE events SET description=?, emotion=?, rating=? WHERE user_id=? AND event_date=?',
            (description, emotion, rating, user_id, event_date)
        )
        await db.commit()

async def get_events_between(user_id: int, start: str, end: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT event_date, description, emotion, rating FROM events WHERE user_id=? AND event_date BETWEEN ? AND ? ORDER BY event_date',
            (user_id, start, end)
        ) as cur:
            return await cur.fetchall()

async def get_best_event(user_id: int, start: str, end: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT event_date, description, emotion, rating FROM events WHERE user_id=? AND event_date BETWEEN ? AND ? ORDER BY rating DESC LIMIT 1',
            (user_id, start, end)
        ) as cur:
            return await cur.fetchone()
