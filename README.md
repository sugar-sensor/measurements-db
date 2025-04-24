## Description
SQLite3 database for sensor measurements. Contains code to import reference data from CSV and generate intermediate reference values for the sensor measured results. It should contain all the data required for the analysis.

## Structure

### Tables

* **tests** - contains BioZ and AFE test time and reference value. Each line is 1 test. Primary table to work with.
* **test_data** - data for the tests. There are multiple results linked to 1 test. One BioZ test contains ~10 key-value pairs representing resistance on different frequencies. Optical test is ~5 key-value pairs representing AFE measurements
* **ref_data** - reference data from invasive sensor

### BioZ test structure

### Optical test structure

