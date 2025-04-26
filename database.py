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

def get_empty_test(conn):
    """ Finds first test with reference = 0 and returns timestamp or 0 """
    sql = 'SELECT min(timestamp) from tests WHERE reference = 0'
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()

    # Return the timestamp if found, otherwise return 0
    return result[0] if result and result[0] is not None else 0

def get_min_reference(conn, ttime):
    """ Finds closest minimal reference value from ref_data table or 0 """
    sql = 'SELECT max(timestamp) from ref_data WHERE timestamp <= ?'
    cur = conn.cursor()
    cur.execute(sql, (ttime,))  # Pass ttime as a tuple with a single element
    result = cur.fetchone()

    # Return the timestamp if found, otherwise return 0
    return result[0] if result and result[0] is not None else 0

def get_next_min_reference(conn, ttime):
    """ Finds next minimal reference value from ref_data table or 0 """
    sql = 'select timestamp from ref_data where timestamp >= ? order by ref_data.timestamp limit 1 offset 1'
    cur = conn.cursor()
    cur.execute(sql, (ttime,))
    result = cur.fetchone()

    return result[0] if result and result[0] is not None else 0

def get_tests_in_range(conn, tmin, tmax):
    """ Return number of tests between tmin and tmax """
    sql = 'select timestamp from tests where timestamp >= ? and timestamp <= ? order by timestamp'
    cur = conn.cursor()
    cur.execute(sql, (tmin,tmax))
    return [row[0] for row in cur.fetchall()]

def get_ref_value(conn, ttime):
    """ Returns reference value by timestamp """
    sql = 'select value from ref_data where timestamp == ?'
    cur = conn.cursor()
    cur.execute(sql, (ttime,))
    return cur.fetchone()[0]

def update_test_ref(conn, ttime, value):
    """ Updates test reference value by timestamp """
    sql = 'UPDATE tests set reference = ? where timestamp = ?'
    cur = conn.cursor()
    cur.execute(sql, (value, ttime))

    conn.commit()