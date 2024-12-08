import sqlite3
from datetime import datetime

from database import *

def loader(conn, filename, test_time):
    # Use a breakpoint in the code line below to debug your script.

    pass


# Entry point
if __name__ == '__main__':
    conn = None
    filename = "test.csv"
    test_time = datetime(2024,11,30,11,0,0) # time of the test
    print('Time:', test_time)
    try:
        conn = sqlite3.connect("measurements.sqlite")
        print(sqlite3.sqlite_version)
        loader(conn, filename, test_time)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()