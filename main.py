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
            if row[7] == "High":
                ref_value = 23
            elif row[7] == "Low":
                ref_value = 2
            else:
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
                print ("\ninvalid data: {}".format(row))
                continue
            test_data = parse_data(row, time_diff)
            test_data.ttype = ttype
            insert_measurement(connection, test_data)
            idx = idx + 1

def parse_test_time(filename):
    # Extract date and time parts from the filename
    # Format: YYMMDD-HHMMSS-*.csv
    parts = filename.split('-')
    if len(parts) < 2:
        # Return current datetime if format is invalid
        return datetime.now()

    date_part = parts[0]  # YYMMDD
    time_part = parts[1]  # HHMMSS

    # Parse date: YYMMDD
    year = 2000 + int(date_part[0:2])  # Assuming 20xx for year
    month = int(date_part[2:4])
    day = int(date_part[4:6])

    # Parse time: HHMMSS
    hour = int(time_part[0:2])
    minute = int(time_part[2:4])
    second = int(time_part[4:6])

    # Create and return datetime object
    return datetime(year, month, day, hour, minute, second)

def update_refs(db):
    # Updates reference value in tests table from ref_data table based on timestamp
    # Test data is sampled more often than reference data. We can use linear approximation
    # to calculate test data vales by dividing difference between ref values by number of test samples
    empty = get_empty_test(db)
    closest_ref = get_min_reference(db, empty)
    next_ref = get_next_min_reference(db, closest_ref)
    tests_num = get_tests_num(db, closest_ref, next_ref)

    print("Min test: {}".format(empty))
    print("Closest ref: {}".format(closest_ref))
    print("Next ref:{}".format(next_ref))
    print("Tests num: {}".format(tests_num))
    # TODO update cycle
    pass

# Entry point
if __name__ == '__main__':
    test = "" # set file name to parse tests
    ref = "" # set reference file to parse, empty to Skip
    test_time = parse_test_time(test)
    test_type = 1 if "muff" in test else 0 # Look Test class description

    print("Test time:", test_time)
    conn = None
    try:
        conn = sqlite3.connect("measurements.sqlite")

        # parse test-data with ref=0 if any
        if len(test) > 0:
            test_data_loader(conn, test, test_type, test_time)
        else:
            print("No test file found. Skipping.")

        # parse ref-data and save it to separate table if any
        if len(ref) > 0:
            ref_data_loader(conn, ref)
        else:
            print("No reference file found. Skipping.")

        # update ref values at tests table from ref_data table
        update_refs(conn)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
