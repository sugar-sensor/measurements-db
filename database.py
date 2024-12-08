from typing import List

class TestData:
    def __init__(self, timestamp: int, parameter: int, value: int):
        self.timestamp = timestamp
        self.parameter = parameter
        self.value = value

class Test:
    def __init__(self, timestamp, mtype, reference, test_data: List[TestData]):
        self.timestamp = timestamp
        self.mtype = mtype
        self.reference = reference
        self.test_data = test_data


def insert_measurement(conn, test: Test):
    """ Inserts measurement with test data into sqlite database """
    sql = 'INSERT INTO tests (timestamp, mtype, reference) VALUES (?, ?, ?)'
    data_sql = 'INSERT INTO test_data (timestamp, parameter, value) VALUES (?, ?, ?)'
    cur = conn.cursor()
    cur.execute(sql, (test.timestamp, test.mtype, test.reference))
    for data in test.test_data:
        cur.execute(data_sql, (data.timestamp, data.parameter, data.value))

    conn.commit()