import click
import os
import requests
import json
import re

api_endpoint = "https://api.github.com/gists"
base_path = "./data/"


def makedir(path: str = ""):
    if not os.path.exists(base_path + path):
        os.makedirs(base_path + path)


def download_file(path: str, url: str, file_name):
    makedir(path)
    file_content = requests.get(url)
    f = open(base_path + path + "/" + file_name, "w")
    f.write(file_content.raw)
    f.close()


def get_gist_content(gist: json):
    user_id: str = str(gist["owner"]["id"])
    login: str = gist["owner"]["login"]
    gist_id: str = gist["id"]
    regex_base = "https://gist.githubusercontent.com/" + login + "/" + gist_id + "/raw/|/"

    for x in gist["files"]:
        file_name = gist["files"][x]["filename"]
        raw_url = gist["files"][x]["raw_url"]
        file_id = re.sub(regex_base + file_name, '', raw_url)
        download_file(user_id + "/" + gist_id + "/" + file_id, raw_url, file_name)


if __name__ == '__main__':
    print("Getting data from api")
    data: requests.api = requests.get(api_endpoint)
    print("Loading data")
    try:
        gists: json = json.loads(data.text)
        if len(gists) <= 2:
            print(gists["message"])
            print(gists["documentation_url"])
            print("SYS > You can bypass this system with proxychain")
            exit(1)
        for el in gists:
            get_gist_content(el)
            exit()
    except json.JSONDecodeError:
        print("Error decoding json. Data :")
        print(data.text)
        exit(1)
