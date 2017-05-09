import logging

import sys
# prints whether python is version 3 or not
python_version = sys.version_info.major
if python_version < 3:
    # url: http://stackoverflow.com/questions/5074225/python-unexpected-eof-while-parsing
    from future.builtins import input

logging.basicConfig(filename='resavion.log', level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')


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

    if message:
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


def choisir_paginer(liste_choix, message="", pas=10):
    """
    Methode qui permet de mettre une pagination 
    
    :param liste_choix: liste des choix a paginer
    :param message: message a dire
    :param pas: 
    :return: 
    """

    borne_bas = 0
    elem = None
    while True:
        borne_haut = min(len(liste_choix), borne_bas + pas)
        # On affiche seulement quelques éléments à la fois
        liste      = liste_choix[borne_bas:borne_haut]
        if borne_bas > 0:
            liste.append("Voir les éléments précédents")
        if borne_haut < len(liste_choix):
            liste.append("Voir les éléments suivants")
        # Faire le choix
        elem = choisir(liste, message)
        if elem == "Voir les éléments suivants":
            borne_bas = borne_haut
        elif elem == "Voir les éléments précédents":
            borne_haut = borne_bas
            borne_bas -= pas
        else:  # On a choisi un élément
            break
    return elem


def afficher_paginer(liste_elems, message, pas=10):
    """
    Methode qui permet d'afficher la pagination
    
   :param liste_choix: liste des choix a paginer
    :param message: message a dire
    :param pas: 
    :return: 
    """
    borne_bas = 0
    elem = None
    while True:
        borne_haut = min(len(liste_elems), borne_bas + pas)
        # On affiche seulement quelques éléments à la fois
        elems      = liste_elems[borne_bas:borne_haut]
        print("{} {} à {}/{} :".format(message, borne_bas, borne_haut,
                                       len(liste_elems)))
        for elem in elems:
            print(elem)
        liste_choix = []
        if borne_bas > 0:
            liste_choix.append("Voir les éléments précédents")
        if borne_haut < len(liste_elems):
            liste_choix.append("Voir les éléments suivants")
        liste_choix.append("Revenir au menu")
        # Faire le choix
        elem = choisir(liste_choix)
        if elem == "Voir les éléments suivants":
            borne_bas = borne_haut
        elif elem == "Voir les éléments précédents":
            borne_haut = borne_bas
            borne_bas -= pas
        else:  # On a choisi un élément
            break
    return elem


def demander(msg):
    """
    Méthode pour demander à l'utilisateur de saisir un texte

    :param msg: question à afficher
    :return: texte saisi par le joueur
    """
    return input(msg)
