# Vaccine

## Description
This program allow you to detect if a website contains some basics sql injection

## Installation
pip install requirements.txt

## Arguments
METHOD: GET/POST
URL: url of the website
output: name of the output file

## Usage :
```python vaccine.py -X METHOD URL -o output```

## Examples
```python vaccine.py -X POST http://localhost:4280/vulnerabilities/sqli -o logs```

## License
[MIT](https://choosealicense.com/licenses/mit/)