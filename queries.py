import sqlite3

#using conn.execute to run sql commands in python
def summary_by_type(conn: sqlite3.Connection) -> None:
    rows = conn.execute("""
                        
    SELECT type, COUNT(*) as count, ROUND(SUM(fee) / 1000000000.0, 6) as total_fees_sol
FROM transactions GROUP BY type ORDER BY count DESC
                        """).fetchall()
    
    pretty_table(rows, title="Transactions by type")
   
                        

#recent transactions
def recent_transactions(conn: sqlite3.Connection, n: int = 10) -> None:
    rows = conn.execute("""
    SELECT substr(signature, 1, 8) || '...' as signature
, datetime(block_time, 'unixepoch') as time,
       type, token_in, amount_in, token_out, amount_out, ROUND(fee / 1000000000.0, 6) as fee_sol
FROM transactions ORDER BY block_time DESC LIMIT ?

    """, (n,)).fetchall()
    pretty_table(rows, title="Recent Transactions")

# failed transactions
def failed_transactions(conn: sqlite3.Connection) -> None:
    rows = conn.execute("""
    SELECT signature, datetime(block_time, 'unixepoch'), description
                        FROM transactions WHERE status = 'failed'
                        """).fetchall()
    pretty_table(rows, title="failed Transactions")

#take data to be printed in readable grid
def pretty_table(rows: list[sqlite3.Row], title: str = "") -> None:
    if not rows:
        print("No results")
        return


    headers = list(rows[0].keys())
    widths = [max(len(headers[i]), max(len(str(row[i])) for row in rows)) for i in range(len(headers))]

    print(f"\n{title}")
    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("  ".join("-" * w for w in widths))

    def fmt(val):
        if isinstance(val, float):
            return f"{val:.6f}"
        return str(val)

    for row in rows:
        print("  ".join(fmt(row[i]).ljust(widths[i]) for i in range(len(headers))))

