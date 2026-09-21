import json
import sqlite3
from pathlib import Path


ROOT = Path(r"D:\Mini_project\Impementation\agent-memory")


def inspect_database(path: Path) -> None:
    print(f"\n=== {path.name} ===")
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    tables = [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        )
    ]
    print("tables:", ", ".join(tables))
    for table in tables:
        if table.startswith("sqlite_"):
            continue
        try:
            count = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            print(f"{table}: {count}")
        except sqlite3.DatabaseError as error:
            print(f"{table}: {error}")
    connection.close()


def inspect_chroma() -> None:
    path = ROOT / "chroma_db" / "chroma.sqlite3"
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    print("\n=== Chroma documents containing travel/train ===")
    query = """
        SELECT e.embedding_id, em.string_value AS document
        FROM embeddings e
        JOIN embedding_metadata em ON em.id = e.id
        WHERE em.key = 'data'
          AND (lower(em.string_value) LIKE '%train%'
               OR lower(em.string_value) LIKE '%bangalore%')
        ORDER BY e.id
    """
    for row in connection.execute(query):
        print(json.dumps(dict(row), ensure_ascii=True))
    connection.close()


def inspect_chat() -> None:
    path = ROOT / "research_data" / "chat_history.sqlite3"
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    print("\n=== Recent chat messages ===")
    query = """
        SELECT s.title, m.role, m.status, m.created_at, m.content
        FROM chat_messages m
        JOIN chat_sessions s USING(session_id)
        ORDER BY m.rowid DESC
        LIMIT 12
    """
    for row in reversed(connection.execute(query).fetchall()):
        value = dict(row)
        value["content"] = value["content"][:220]
        print(json.dumps(value, ensure_ascii=True))
    connection.close()


def inspect_mem0_history() -> None:
    path = ROOT / "research_data" / "mem0_history.db"
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    print("\n=== Recent Mem0 history ===")
    columns = [row[1] for row in connection.execute("PRAGMA table_info(history)")]
    print("history_columns:", columns)
    rows = connection.execute("SELECT * FROM history ORDER BY rowid DESC LIMIT 12").fetchall()
    for row in reversed(rows):
        value = dict(row)
        for key, item in list(value.items()):
            if isinstance(item, str) and len(item) > 300:
                value[key] = item[:300]
        print(json.dumps(value, ensure_ascii=True, default=str))
    connection.close()


if __name__ == "__main__":
    inspect_database(ROOT / "chroma_db" / "chroma.sqlite3")
    inspect_database(ROOT / "research_data" / "mem0_history.db")
    inspect_database(ROOT / "research_data" / "usage.sqlite3")
    inspect_database(ROOT / "research_data" / "chat_history.sqlite3")
    inspect_chroma()
    inspect_mem0_history()
    inspect_chat()
