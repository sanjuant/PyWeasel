import glob
import os
import re
import time
from datetime import timedelta

import pandas as pd
import numpy as np


def find_files_in_folder_yield(path, extension, contains_txt='', sub_folders=True, exclude_text=''):
    """  Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

    path:               Base directory to find files
    extension:          File extension to find.  e.g. 'txt'.  Regular expression. Or  'ls\d' to match ls1, ls2, ls3 etc
    containsTxt:        List of Strings, only finds file if it contains this text.  Ignore if '' (or blank)
    subFolders:         Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
    excludeText:        Text string.  Ignore if ''. Will exclude if text string is in path.
    """
    if type(contains_txt) == str:  # if a string and not in a list
        contains_txt = [contains_txt]

    my_regex_obj = re.compile(
        '\.' + extension + '$')  # Makes sure the file extension is at the end and is preceded by a .

    try:  # Trapping a OSError or FileNotFoundError:  File permissions problem I believe
        for entry in os.scandir(path):
            if entry.is_file() and my_regex_obj.search(entry.path):  #
                bools = [True for txt in contains_txt if
                         txt in entry.path and (exclude_text == '' or exclude_text not in entry.path)]
                if len(bools) == len(contains_txt):
                    yield entry.stat().st_size, entry.stat().st_atime_ns, entry.stat().st_mtime_ns, entry.stat().st_ctime_ns, os.path.normpath(
                        entry.path)

            elif entry.is_dir() and sub_folders:  # if its a directory, then repeat process as a nested function
                yield from find_files_in_folder_yield(entry.path, extension, contains_txt, sub_folders)
    except FileNotFoundError as fnf:
        print(path + ' not found ', fnf)
    except OSError as ose:
        print('Cannot access ' + path + '. Probably a permissions error ', ose)


def find_path_of_files_in_folder_yield(path, extension, contains_txt='', sub_folders=True, exclude_text=''):
    """  Converts returned data from findFilesInFolderYield and creates and Pandas Dataframe.
    Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

    path:               Base directory to find files
    extension:          File extension to find.  e.g. 'txt'.  Regular expression. Or  'ls\d' to match ls1, ls2, ls3 etc
    containsTxt:        List of Strings, only finds file if it contains this text.  Ignore if '' (or blank)
    subFolders:         Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
    excludeText:        Text string.  Ignore if ''. Will exclude if text string is in path.
    """

    fileSizes, accessTimes, modificationTimes, creationTimes, paths = zip(
        *find_files_in_folder_yield(path, extension, contains_txt, sub_folders, exclude_text))
    # df = pd.DataFrame({
    #     'FLS_File_Size': fileSizes,
    #     'FLS_File_Access_Date': accessTimes,
    #     'FLS_File_Modification_Date': np.array(modificationTimes).astype('timedelta64[ns]'),
    #     'FLS_File_Creation_Date': creationTimes,
    #     'FLS_File_PathName': paths,
    # })

    # df['FLS_File_Modification_Date'] = pd.to_datetime(df['FLS_File_Modification_Date'], infer_datetime_format=True)
    # df['FLS_File_Creation_Date'] = pd.to_datetime(df['FLS_File_Creation_Date'], infer_datetime_format=True)
    # df['FLS_File_Access_Date'] = pd.to_datetime(df['FLS_File_Access_Date'], infer_datetime_format=True)

    return paths


# ext = 'txt'  # regular expression
# containsTxt = []
# path = 'C:\myFolder'
# df = findFilesInFolderYieldandGetDf(path, ext, containsTxt, subFolders=True)


def stopwatch(method):
    def timed(*args, **kw):
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        duration = timedelta(seconds=te - ts)
        print(f"{method.__name__}: {duration}")
        return result

    return timed


@stopwatch
def get_filepaths_with_oswalk(root_path: str, file_regex: str):
    files_paths = []
    pattern = re.compile(file_regex)
    for root, directories, files in os.walk(root_path):
        for file in files:
            if pattern.match(file):
                files_paths.append(os.path.join(root, file))
    return files_paths


@stopwatch
def get_filepaths_with_glob(root_path: str, file_regex: str):
    return glob.glob(os.path.join(root_path, file_regex))
