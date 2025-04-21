CREATE TABLE IF NOT EXISTS tests (
    timestamp integer primary key,
    ttype integer not null,
    mtype integer not null,
    reference real
);

CREATE TABLE IF NOT EXISTS test_data (
    id integer primary key autoincrement,
    timestamp integer not null,
    parameter integer not null,
    value integer not null,
    foreign key (timestamp) references tests (timestamp)
);

CREATE TABLE IF NOT EXISTS ref_data (
    timestamp integer not null,
    value real not null
);

CREATE INDEX IF NOT EXISTS test_data_idx on test_data (timestamp);
CREATE UNIQUE INDEX IF NOT EXISTS ref_data_idx on ref_data (timestamp);