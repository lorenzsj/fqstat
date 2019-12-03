# fqstat
Recursively find FastQ files and report the percent of records with nucleotides greater than a provided value per file.

## Dependencies
* Python3.6
* BioPython
* prettytable

## Installation
It is recommended that fqstat be installed in a new virtual python environment. For example,
```bash
virtualenv -p python3 env
source env/bin/activate
```
Then, move into the project directory and run the following command:
```bash
cd fqstat/
pip install -e .
```
This will install fqstat as a package along with all of it's dependencies using setuptools. The -e flag is optional and simply allows the package to be modified without reinstallation.

fqstat can also be run without being installed as a package. For example,
```bash
python fqstat/fqstat.py
usage: fqstat.py [-h] [--pattern PATTERN] [--nucleotides INT] [--quiet]
                 root_dir
fqstat.py: error: the following arguments are required: root_dir
```

## Usage
fqstat requires 1 positional argument referred to as the root_dir which is used as the starting point of the search. It also supports the following optional parameters:

| Flag          | Description                                     |
| ------------- | ----------------------------------------------- |
| --pattern     | string used to match files during the search    |
| --nucleotides | number of nucleotides used as the cutoff point. |
| --quiet       | do not print results                            |

### Defaults

| Flag          | Description                                         |
| ------------- | --------------------------------------------------- |
| --pattern     | **/\*.fqstat (recursively find all \*.fqstat files) |
| --nucleotides | 30                                                  |
| --quiet       | False                                               |

### Examples
Find all the \*.fqstat files in the current directory.
```bash
fqstat '.'
```

Set the number of nucleotides to be greater than 50.
```bash
fqstat '.' --nucleotides 50
```
