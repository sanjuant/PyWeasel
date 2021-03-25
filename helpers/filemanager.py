import csv
import getpass
import os
import re
import shutil
import socket
import sys

from pip._vendor import requests
from slugify import slugify

from helpers import find_files, csv_manager


def search_files(files, path='', contains_txt='', exclude_text=''):
    files_found = []
    search_files_regex = '|'.join([re.escape(file) for file in files])
    if os.name == "nt":
        if path == '':
            for i in drives_letter():
                files_found += find_files.find_path_of_files_in_folder_yield(i + ':/', search_files_regex, contains_txt,
                                                                             True, exclude_text)
        else:
            files_found += find_files.find_path_of_files_in_folder_yield(path, search_files_regex, contains_txt, True,
                                                                         exclude_text)
        return files_found
    elif os.name == "posix":
        path = '/' if path == '' else path
        files_found += find_files.glob_re(path, search_files_regex)
        return files_found


def sfiles_dir_exist():
    db_path = os.path.join('.', 'sfiles')
    if not os.path.isdir(db_path):
        os.makedirs(db_path)
    return db_path


def drives_letter():
    return ''.join(
        l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:/' % l)) if sys.platform == 'win32' else ''


def copy_files(files):
    filenames = []
    prefix = socket.gethostname() + '_' + getpass.getuser() + '_'
    for file in files:
        if os.path.normpath("PyWeasel") not in file and os.stat(file).st_size >= 1:
            filename = slugify(file)
            shutil.copy(file, os.path.join(sfiles_dir_exist(), filename))
            filenames.append((file, filename))
    return filenames


def send_files(url):
    links = []
    # open file in read mode
    with open(csv_manager.FILENAME, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.DictReader(read_obj, fieldnames=csv_manager.FIELDS, delimiter=';')
        # Iterate over each row in the csv using reader object
        idx = 0
        for row in csv_reader:
            idx += 1
            if idx > 1:
                with open('sfiles/' + row['filename'], 'rb') as f:
                    r = requests.post(url, files={row['filename']: f})
                    links.append((row['filename'], r.json()['body'][row['filename']]['url']))
    return links
