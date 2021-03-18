import os
from pip._vendor import requests


def send_file(url):
    for filename in os.listdir("sfiles"):
        with open('sfiles/' + filename, 'rb') as f:
            r = requests.post(url, files={filename: f})
            save_print(filename + ' ; ' + r.json()['body'][filename]['url'])