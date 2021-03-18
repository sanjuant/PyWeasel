import csv
import os

from helpers import utils

FILENAME = "sfiles.csv"
FIELDS = ['hostname', 'ip', 'proc', 'system', 'os_name', 'machine', 'username', 'file', 'filename']


def init():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w', newline='') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            # writing headers (field names)
            writer.writeheader()
            return writer
    else:
        with open(FILENAME, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            # writer.writerow(system_information)
            return writer


def get_writer():
    with open(FILENAME, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        return writer


def add_rows(files):
    system_information = utils.system_information().copy()
    data = system_information
    with open(FILENAME, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    # writer.writerow(system_information)
        for file in files:
            data['file'] = file[0]
            data['filename'] = file[1]
            writer.writerow(data)
