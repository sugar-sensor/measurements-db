import csv
import re
import sqlite3

from datetime import datetime
from tqdm import tqdm

from database import *

def parse_data(data, time_diff):
    time = int(data[0]) + time_diff
    type = int(data[1])
    pairs = re.findall(r"\((\d+,\d+)\)", data[2])
    test_data: List[TestData] = []
    for pair in pairs:
        parsed = pair.split(',')
        test_data.append(TestData(time, int(parsed[0]), int(parsed[1])))

    test = Test(time, type, 0, test_data)
    return test


def loader(conn, filename, test_time):

    # Open CSV and read it line by line
    # Example data is:
    # 1732572000
    # ['1732572004', '1', '(0,524288)-(1,611668)-(2,349525)-(3,786429)-(4,786429)-(5,611666)-(6,786427)-(7,436899)-(8,524271)-(9,436911)-(10,87636)']
    # ['1732572007', '0', '(8,2547)-(2,1729)-(7,26)-(1,99)']

    with open(filename, mode="r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        idx = 0
        for row in tqdm(csv_reader):
            if idx == 0:
                sample_time = row[0] # start time
            time_diff = test_time.timestamp() - int(sample_time)
            if len(row) != 3:
                print ("invalid data: {}".format(row))
                continue
            test = parse_data(row, time_diff)
            insert_measurement(conn, test)
            idx = idx + 1

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
