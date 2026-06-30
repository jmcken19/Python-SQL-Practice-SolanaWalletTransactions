import sqlite3
from config import DB_PATH


#Creates a connection to SQLite database
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row 
    return conn

# Creates schema in database
def create_schema(conn: sqlite3.Connection) -> None:
    # The SQL is stored in a variable called 'sql' below.
    # conn.execute(sql) sends it to the database.
    sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            signature   TEXT PRIMARY KEY,
            block_time  INTEGER,
            slot        INTEGER,
            fee         INTEGER,
            status      TEXT,
            source      TEXT,
            type        TEXT,
            description TEXT,
            token_in    TEXT,
            token_out   TEXT,
            amount_out  REAL,
            amount_in   REAL
        )
    """
    conn.execute(sql)
    conn.commit()



def insert_transactions(conn: sqlite3.Connection, rows: list[dict]) -> int:
    # The SQL uses ? as safe placeholders — sqlite3 fills them in from your tuple.
    # INSERT OR IGNORE means re-running this won't crash on duplicate signatures.
    sql = """
        INSERT OR IGNORE INTO transactions
            (signature, block_time, slot, fee, status, source, type, description, token_in, token_out, amount_out, amount_in)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # tuples is a list where each item maps to one row in the database.
    # The value order must match the column order in the SQL above.
    tuples = [
        (
            row["signature"],
            row["block_time"],
            row["slot"],
            row["fee"],
            row["status"],
            row["source"],
            row["type"],
            row["description"],
            row["token_in"],
            row["token_out"],
            row["amount_out"],
            row["amount_in"],
            
        )
        for row in rows
    ]

    # executemany(sql, tuples) runs the SQL once per tuple, much faster than a loop.
    cursor = conn.executemany(sql, tuples)
    conn.commit()
    return cursor.rowcount
