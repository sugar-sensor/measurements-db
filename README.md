## Description
SQLite3 database for sensor measurements. Contains code to import reference data from CSV and generate intermediate reference values for the sensor measured results. It should contain all the data required for the analysis.

## Structure

### Tables

* **tests** - contains BioZ and AFE test time and reference value. Each line is 1 test. Primary table to work with.
* **test_data** - data for the tests. There are multiple results linked to 1 test. One BioZ test contains ~10 key-value pairs representing resistance on different frequencies. Optical test is ~5 key-value pairs representing AFE measurements
* **ref_data** - reference data from invasive sensor

### BioZ test structure
BioZ MAX30002 chip configured to measure 10 impedance values on different frequencies configured by values from 0 to 10 in fcgen register. 
Frequencies to measure on are in the following table:

| fcgen | frequency |
|-------|-----------|
| 0     | 128 kHz   |
| 1     | 80 kHz    |
| 2     | 40 kHz    |
| 3     | 18 kHz    |
| 4     | 8 kHz     |
| 5     | 4 kHz     |
| 6     | 2 kHz     |
| 7     | 1000 Hz   |
| 8     | 500 Hz    |
| 9     | 250 Hz    |
| 10    | 125 Hz    |


### Optical test structure
Optical AFE is built on MAX86140 chip and gives the following measurements based on **tag**

| tag | data type | comments |
|-----|-----------|----------|
| 1   | PPG1 LEDC1 DATA | If LEDC1 is non-zero|
| 2   | PPG1 LEDC2 DATA | If LEDC1 and LEDC2 are non-zero|
| 7   | PPG2 LEDC2 DATA | If LEDC1 is non-zero|
| 8   | PPG2 LEDC2 DATA | If LEDC1 and LEDC2 are non-zero|
