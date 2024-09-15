# Vaccine 🧑🏼‍🔬

## Description
Vaccine is a tool that automates the process of detecting and exploiting SQL injection with GET and POST methods

## Installation
pip install requirements.txt

## Arguments
- METHOD: http method used by the form GET/POST
- URL: url of the website
- output: name of the output file

## Usage
```bash 
python vaccine.py -X METHOD URL -o output
```

## Examples
```bash
python vaccine.py -X POST http://localhost:4280/vulnerabilities/sqli -o logs
```

## License
[MIT](https://choosealicense.com/licenses/mit/)