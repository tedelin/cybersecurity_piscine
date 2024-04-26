import os
from termcolor import colored
import requests
from bs4 import BeautifulSoup
import argparse
import uuid
from datetime import datetime

parser = argparse.ArgumentParser(description="Spider extract all the images from a website")
parser.add_argument("url", help="The URL of the website to extract images")
parser.add_argument("-r", action="store_true", help="Extract images recursively")
parser.add_argument("-l", type=int, help="The maximum number of levels to extract images")
parser.add_argument("-p", help="The path to save the images")
args = parser.parse_args()

file_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
already_visited = []
img_folder = "data" if not args.p else args.p
if not os.path.exists(img_folder):
    os.makedirs(img_folder)

level = 5
if args.r:
	level = 5
if args.l and args.r:
	level = args.l
def generate_unique_name(ext):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:6] 
    return f"{timestamp}_{unique_id}.{ext}"

def spider(url, lvl):
	if (lvl == -1):
		return
	already_visited.append(url)
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	pages = soup.find_all("a")
	img_tags = soup.find_all("img")
	print(colored("current level:", 'red'), lvl, colored("visiting:", 'blue'),url, colored("links found:", 'green'), len(pages), colored("images found:", 'red'), len(img_tags))
	for img_tag in img_tags:
		src = img_tag.get("src")
		if src:
			if (src.startswith("//")):
				src = "https:" + src
			elif (src.startswith("/")):
				end = url.find("/", url.find("://") + 3)
				if (end == -1):
					end = len(url)
				src = url[:end] + src
			elif (src.startswith("http") == 0):
				src = args.url + src
			image_response = requests.get(src)
			if (src.endswith(tuple(file_extensions)) and image_response.status_code == 200):
				filename = img_folder + "/" + generate_unique_name(src.split(".")[-1])
				with open(filename, 'wb') as f:
					f.write(image_response.content)
	for page in pages:
		new_url = page.get("href")
		if new_url and new_url not in already_visited:
			if (new_url.startswith("http") == 0):
					new_url = url + new_url
			spider(new_url, lvl - 1)

print(level)
spider(args.url, level)