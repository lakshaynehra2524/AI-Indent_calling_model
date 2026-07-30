import json
import sqlite3
from contextlib import closing

from .config import DB_PATH


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with closing(_connect()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                text TEXT NOT NULL,
                intent TEXT NOT NULL,
                confidence REAL NOT NULL,
                entities TEXT NOT NULL,
                route TEXT NOT NULL
            )
            """
        )
        conn.commit()


def log_prediction(text, intent, confidence, entities, route):
    init_db()
    with closing(_connect()) as conn:
        conn.execute(
            """
            INSERT INTO predictions (timestamp, text, intent, confidence, entities, route)
            VALUES (datetime('now'), ?, ?, ?, ?, ?)
            """,
            (text, intent, confidence, json.dumps(entities), route),
        )
        conn.commit()


def get_recent(limit=10):
    init_db()
    with closing(_connect()) as conn:
        rows = conn.execute(
            """
            SELECT timestamp, text, intent, confidence, entities, route
            FROM predictions ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "timestamp": row[0],
            "text": row[1],
            "intent": row[2],
            "confidence": row[3],
            "entities": json.loads(row[4]),
            "route": row[5],
        }
        for row in rows
    ]


def get_stats():
    init_db()
    with closing(_connect()) as conn:
        total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        by_intent = conn.execute(
            "SELECT intent, COUNT(*) FROM predictions GROUP BY intent ORDER BY COUNT(*) DESC"
        ).fetchall()
        avg_confidence = conn.execute(
            "SELECT AVG(confidence) FROM predictions"
        ).fetchone()[0]
        fallback_count = conn.execute(
            "SELECT COUNT(*) FROM predictions WHERE route = 'home'"
        ).fetchone()[0]

    return {
        "total": total,
        "by_intent": dict(by_intent),
        "avg_confidence": avg_confidence or 0.0,
        "fallback_count": fallback_count,
    }
