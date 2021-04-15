import os
import re
from pathlib import Path


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

    my_regex_obj = re.compile(extension + '$')  # Makes sure the file extension is at the end and is preceded by a .

    try:  # Trapping a OSError or FileNotFoundError:  File permissions problem I believe
        for entry in os.scandir(path):
            if entry.is_file() and my_regex_obj.search(entry.path):  #
                bools = [True for txt in contains_txt if
                         txt in entry.path and (exclude_text == '' or exclude_text not in entry.path)]
                if len(bools):
                    yield os.path.normpath(entry.path)

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
    return find_files_in_folder_yield(path, extension, contains_txt, sub_folders, exclude_text)


# ext = 'txt'  # regular expression
# containsTxt = []
# path = 'C:\myFolder'
# df = findFilesInFolderYieldandGetDf(path, ext, containsTxt, subFolders=True)

def glob_re(path, regex="", glob_mask="**/*", inverse=False):
    p = Path(path)
    if inverse:
        res = [str(f) for f in p.glob(glob_mask) if not re.search(regex, str(f))]
    else:
        res = [str(f) for f in p.glob(glob_mask) if re.search(regex, str(f))]
    print(res)
    return res
