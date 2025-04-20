from typing import List

class TestData:
    def __init__(self, timestamp: int, parameter: int, value: int):
        self.timestamp = timestamp
        self.parameter = parameter
        self.value = value

class Test:
    def __init__(self, timestamp, ttype, mtype, reference, test_data: List[TestData]):
        self.timestamp = timestamp
        self.ttype = ttype # test type: 0 - full test (bioz + optical), 1 - optical with muff
        self.mtype = mtype # measurement type: 0 - optical, 1 - bioz
        self.reference = reference
        self.test_data = test_data


def insert_measurement(conn, test: Test):
    """ Inserts measurement with test data into sqlite database """
    sql = 'INSERT INTO tests (timestamp, ttype, mtype, reference) VALUES (?, ?, ?, ?)'
    data_sql = 'INSERT INTO test_data (timestamp, parameter, value) VALUES (?, ?, ?)'
    cur = conn.cursor()
    cur.execute(sql, (test.timestamp, test.ttype, test.mtype, test.reference))
    for data in test.test_data:
        cur.execute(data_sql, (data.timestamp, data.parameter, data.value))

    conn.commit()

def insert_ref(conn, time, value):
    """ Inserts reference data into sqlite database """
    sql = 'INSERT INTO ref_data (timestamp, value) VALUES (?, ?)'
    cur = conn.cursor()
    cur.execute(sql, (time, value))

    conn.commit()