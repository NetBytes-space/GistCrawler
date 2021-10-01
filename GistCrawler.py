import click
import os
import requests
import json
import re
import sqlite3

api_endpoint = "https://api.github.com/gists"
base_path = "./data/"


def makedir(path: str = ""):
    if not os.path.exists(base_path + path):
        os.makedirs(base_path + path)


def db_get():
    makedir()
    return sqlite3.connect(base_path + "data.db").cursor()


def db_init():
    sql_file = open("setup.sql")
    sql_data = sql_file.read()
    cur = db_get()
    cur.executescript(sql_data)
    cur.close()


def download_file(path: str, url: str, file_name):
    makedir(path)
    file_content = requests.get(url)
    with open(base_path + path + "/" + file_name, "w") as f:
        f.write(str(file_content.content))


def get_gist_content(gist: json):
    user_id: str = str(gist["owner"]["id"])
    login: str = gist["owner"]["login"]
    gist_id: str = gist["id"]
    regex_base = "https://gist.githubusercontent.com/" + login + "/" + gist_id + "/raw/|/"

    for x in gist["files"]:
        file_name = gist["files"][x]["filename"]
        raw_url = gist["files"][x]["raw_url"]
        file_id = re.sub(regex_base + file_name, '', raw_url)
        print(raw_url)
        download_file(user_id + "/" + gist_id + "/" + file_id, raw_url, file_name)


if __name__ == '__main__':
    print("Init database")
    db_init()
    exit(0)
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
    except json.JSONDecodeError:
        print("Error decoding json. Data :")
        print(data.text)
        exit(1)
