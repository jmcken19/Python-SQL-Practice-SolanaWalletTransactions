from db      import get_connection, create_schema, insert_transactions
from helius  import fetch_transactions
from parser  import parse_transactions
import queries


def main() -> None:
    # Step 1 — DB setup
    conn = get_connection()
    create_schema(conn)

    # Step 2 — Fetch
    print("Fetching transactions from Helius...")
    raw = fetch_transactions()
    print(f"  Got {len(raw)} raw records")

    # Step 3 — Parse
    rows = parse_transactions(raw)
    print(f"  Parsed {len(rows)} valid rows")

    # Step 4 — Insert
    inserted = insert_transactions(conn, rows)
    print(f"  Inserted {inserted} new rows into DB\n")

    # Step 5 — Query + display
    queries.summary_by_type(conn)
    queries.recent_transactions(conn)
    queries.failed_transactions(conn)

    conn.close()


if __name__ == "__main__":
    main()
