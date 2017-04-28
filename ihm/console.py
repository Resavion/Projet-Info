import logging

import sys
# prints whether python is version 3 or not
python_version = sys.version_info.major
if python_version < 3:
    # url: http://stackoverflow.com/questions/5074225/python-unexpected-eof-while-parsing
    from future.builtins import input

logging.basicConfig(filename='pokemon.log', level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')


def afficher(msg):
    """
    Affichage d'un message dans la console et log du message dans un fichier

    :param msg: message à afficher+logguer
    """
    print(msg)
    logging.info(msg)


def logger(msg):
    """
    Log d'un message dans un fichier

    :param msg: message à logguer
    """
    logging.info(msg)


def choisir(liste_choix, message=""):
    """
    Méthode de choix d'une action parmi une liste de propositions

    :param liste_choix: liste des choix en entrée
    :param message: question à afficher
    :return: élément de liste_choix retenu par l'utilisateur
    """
    print(message)

    for i, msg_choix in enumerate(liste_choix):
        print("{} : {}".format(i, msg_choix))
    choix = input()

    try:
        choix = liste_choix[int(choix)]
    except (IndexError, TypeError, ValueError):
        choix = choisir(liste_choix)
    finally:
        return choix


def demander(msg):
    """
    Méthode pour demander à l'utilisateur de saisir un texte

    :param msg: question à afficher
    :return: texte saisi par le joueur
    """
    return input(msg)
