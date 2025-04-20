import csv
import re
import sqlite3

from datetime import datetime
from tqdm import tqdm

from database import *

def parse_data(data, time_diff):
    time = int(data[0]) + time_diff
    mtype = int(data[1])
    pairs = re.findall(r"\((\d+,\d+)\)", data[2])
    test_data: List[TestData] = []
    for pair in pairs:
        parsed = pair.split(',')
        test_data.append(TestData(time, int(parsed[0]), int(parsed[1])))

    return Test(time, 0, mtype, 0, test_data)


def ref_data_loader (connection, filename):
    # Example data is:
    # ["11","2024-11-30T00:00:39","EGV","","","","iOS DexcomOne","13.4","","","","","1319474","C2RWZB"]
    with open(filename, mode="r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in tqdm(csv_reader):
            time = datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S")
            ref_value = float(row[7])
            insert_ref(connection, time.timestamp(), ref_value)


def test_data_loader(connection, filename, ttype, ttime):
    # Open CSV and read it line by line
    # Example data is:
    # ['1732572004', '1', '(0,524288)-(1,611668)-(2,349525)-(3,786429)-(4,786429)-(5,611666)-(6,786427)-(7,436899)-(8,524271)-(9,436911)-(10,87636)']
    # ['1732572007', '0', '(8,2547)-(2,1729)-(7,26)-(1,99)']

    with open(filename, mode="r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        idx = 0
        for row in tqdm(csv_reader):
            if idx == 0:
                sample_time = row[0] # start time
            time_diff = ttime.timestamp() - int(sample_time)
            if len(row) != 3:
                print ("invalid data: {}".format(row))
                continue
            test_data = parse_data(row, time_diff)
            test_data.ttype = ttype
            insert_measurement(connection, test_data)
            idx = idx + 1

# Entry point
if __name__ == '__main__':
    conn = None
    test = "test.csv"
    ref = "ref.csv"
    test_type = 0 # default test type is full-test
    test_time = datetime(2024,11,30,11,0,0) # time of the test
    print('Time:', test_time)
    try:
        conn = sqlite3.connect("measurements.sqlite")
        print(sqlite3.sqlite_version)
        # parse test-data with ref=0
        test_data_loader(conn, test, test_type, test_time)
        # parse ref-data and save it to separate table
        ref_data_loader(conn, ref)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
