from bs4 import BeautifulSoup
from difflib import Differ
from requests_html import HTMLSession

session = HTMLSession()


def get_all_forms(url):
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
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
        inputs.append(
            {
                "type": select_type,
                "name": select_name,
                "values": select_options,
                "value": select_default_value,
            }
        )
    for textarea in form.find_all("textarea"):
        textarea_name = textarea.attrs.get("name")
        textarea_type = "textarea"
        textarea_value = textarea.attrs.get("value", "")
        inputs.append(
            {"type": textarea_type, "name": textarea_name, "value": textarea_value}
        )
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def find_first_pos(line):
    x = 0
    white_space = "\t\n\r\t\f "
    for letter in line:
        if white_space.find(letter) != -1:
            x = x + 1
            continue
        return x + 1


def diff_html(html1, html2):
    if html1 == html2:
        return
    result = []
    differ = Differ()
    deltas = list(differ.compare(html1, html2))
    for line in deltas:
        if line.startswith("+") and not line[1:].isspace():
            pos = find_first_pos(line[1:])
            parsed_line = line[pos : len(line) - 1]
            if parsed_line.startswith("<"):
                parsed_line = BeautifulSoup(parsed_line, "html.parser").get_text()
            if len(parsed_line) != 0:
                result.append(parsed_line)
    return result
