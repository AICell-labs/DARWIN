#
#
import logging
import sqlite3
from datetime import datetime

table_log = logging.getLogger(name="table")
table_log.setLevel("DEBUG")
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Modify here
file_handler = logging.FileHandler(f"./log/table-{str(now)}.log",
                                   encoding="utf-8")
file_handler.setLevel("DEBUG")
file_handler.setFormatter(logging.Formatter("%(message)s"))
table_log.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel("DEBUG")
stream_handler.setFormatter(logging.Formatter("%(message)s"))
table_log.addHandler(stream_handler)


def print_db_contents(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve and print all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # print("Tables:", [table[0] for table in tables])
    table_log.info("Tables:" + " ".join([str(table[0]) for table in tables]))

    for table_name in tables:
        # print(f"\nTable: {table_name[0]}")
        table_log.info(f"\nTable: {table_name[0]}")
        # Print table structure
        cursor.execute(f"PRAGMA table_info({table_name[0]})")
        columns = cursor.fetchall()
        # print("Columns:")
        table_log.info("Columns:")
        for col in columns:
            # print(f"  {col[1]} ({col[2]})")
            table_log.info(f"  {col[1]} ({col[2]})")

        # Print table contents
        cursor.execute(f"SELECT * FROM {table_name[0]}")
        rows = cursor.fetchall()
        # print("Contents:")
        table_log.info("Contents:")
        for row in rows:
            # print(" ", row)
            table_log.info(" " + ", ".join(str(item) for item in row))
    # Close the connection
    conn.close()
