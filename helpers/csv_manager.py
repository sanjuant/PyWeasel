import csv
import os
import shutil
from datetime import datetime
from urllib import parse
from helpers import utils


FILENAME = "sfiles.csv"
FIELDS = ['hostname', 'ip', 'proc', 'system', 'os_name', 'machine', 'username', 'file', 'filename', 'expire_date',
          'dl_link']


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


def add_rows(files):
    system_information = utils.system_information().copy()
    data = system_information

    with open(FILENAME, 'r') as csvfile, open('outputfile.csv', 'w', newline='') as output:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(output, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            for file in files.copy():
                if file[0] == row['file'] and file[1] == row['filename']:
                    files.remove(file)
            writer.writerow(row)
        for file in files:
            data['file'] = file[0]
            data['filename'] = file[1]
            data['expire_date'] = ''
            data['dl_link'] = ''
            writer.writerow(data)

    shutil.move('outputfile.csv', FILENAME)


def update_dl_link(dl_links):
    with open(FILENAME, 'r') as csvfile, open('outputfile.csv', 'w', newline='') as output:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(output, fieldnames=FIELDS, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            for link in dl_links:
                if link[0] == row['filename']:
                    row['dl_link'] = link[1]
                    row['expire_date'] = datetime.fromtimestamp(
                        int(parse.parse_qs(parse.urlparse(link[1]).query)['Expires'][0]))
                # write the row either way
            writer.writerow(row)
    shutil.move('outputfile.csv', FILENAME)
