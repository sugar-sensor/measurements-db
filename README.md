## Description
Database for sensor measurements. Contains code to import reference data from CSV and generate intermediate reference values for the sensor measured results. It should contain all the data required for the analysis.

## Structure

### Tables

* **tests** - contains BioZ and AFE test time and reference value. Each line is 1 test.
* **test_data** - data for the tests. One BioZ test contains ~10 key-value pairs representing resistance on different frequencies. Optical test is ~5 key-value pairs representing AFE measurements
* **ref_data** - reference data from invasive sensor
