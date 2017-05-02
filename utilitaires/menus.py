from datetime import datetime

import ihm.console as ihm
from reservation.Client import Client


def actions_client(clients):
    # Choisir un client existant ou nouveau
    comptes = [client for client in clients]
    comptes.append('Nouveau client')
    client = ihm.choisir(
        comptes, "Choisissez un client sauvegardé ou "
                 "créez un nouveau client")

    # Si nouveau : demander infos et créer client
    if client == 'Nouveau client':
        client = ajouter_client(clients)
        clients.append(client)

    # Le client est chargé
    ihm.afficher("Bonjour {} !".format(client.prenom))

    # Demander action : Faire, Consulter, Modifier, Annuler
    actions = ('Faire une réservation', 'Consulter ses réservations',
               'Modifier une réservation', 'Annuler une réservation',
               'Revenir au début')
    action = ihm.choisir(actions, "Choisissez une action :")
    if action == actions[0]:
        client.faire_reservation()
    elif action == actions[1]:
        client.consulter_reservations()
    elif action == actions[2]:
        client.modifier_reservation()
    elif action == actions[3]:
        client.annuler_reservation()
    else:
        pass


def ajouter_client(clients):
    """
    Crée un nouveau client
    
    :param clients: liste des clients existants
    :return: nouveau client
    """
    new_id = clients[-1].id + 1
    nom = ihm.demander("Saisissez votre nom :")
    prenom = ihm.demander("Saisissez votre prénom :")
    while True:
        try:
            date_naiss = ihm.demander(
                "Saisissez votre date de naissance (AAAA-MM-JJ) :")
            date_naiss = datetime.strptime(date_naiss, '%Y-%m-%d')
        except ValueError:
            ihm.afficher("Ceci n'est pas une date valide.")
            pass
        else:
            date_naiss = date_naiss.date()
            break
    client = Client(new_id, nom, prenom, date_naiss)
    return client


def actions_compagnie(compagnies):
    # On demande de choisir une compagnie
    actions = ('Recherche par continent',
               'Recherche par code IATA ou ICAO',
               'Revenir au début')
    recherche = ihm.choisir(actions, "Choisissez un mode de recherche :")

    # Si recherche par continents
    if recherche == actions[0]:
        continents = {'Amérique du Nord': 'NA', 'Amérique du Sud': 'SA',
                      'Europe': 'EU', 'Afrique': 'AF', 'Asie': 'AS',
                      'Océanie': 'OC'}
        nom = ihm.choisir([*continents.keys()],
                          "Choisissez un continent :")
        compagnies.sort(key=lambda s: len(s.routes), reverse=True)
        compagnies_filtre = [x for x in compagnies
                             if x.code_continent == continents[nom]]
        borne_bas = 0
        pas = 2
        compagnie = None
        while True:
            borne_haut = min(len(compagnies_filtre), borne_bas + pas)
            liste = compagnies_filtre[borne_bas:borne_haut]
            if len(liste) == 0:
                ihm.afficher("Il n'y a pas de compagnie disponible !")
                break
            if borne_bas > 0:
                liste.append("Voir les compagnies précédentes")
            if borne_haut < len(compagnies_filtre):
                liste.append("Voir les compagnies suivantes")
            # Faire le choix
            compagnie = ihm.choisir(liste, "Choisissez une compagnie :")
            if compagnie == "Voir les compagnies suivantes":
                borne_bas = borne_haut
            elif compagnie == "Voir les compagnies précédentes":
                borne_haut = borne_bas
                borne_bas -= pas
            else:
                print(compagnie)
                break
    # Si recherche par code
    elif recherche == actions[1]:
        test = True
    # Sinon on revient au début
    else:
        pass


def choisir_par_continent(compagnies):
    # On choisit un continent
    continents = {'Amérique du Nord': 'NA', 'Amérique du Sud': 'SA',
                  'Europe': 'EU', 'Afrique': 'AF', 'Asie': 'AS',
                  'Océanie': 'OC'}
    nom = ihm.choisir([*continents.keys()],
                      "Choisissez un continent :")

    # On ne garde que les compagnies du continent
    compagnies_filtre = [x for x in compagnies
                         if x.code_continent == continents[nom]]
    if len(compagnies_filtre) == 0:
        ihm.afficher("Il n'y a pas de compagnie disponible !")
        return None

    # On filtre les compagnies par nombre de routes
    compagnies_filtre.sort(key=lambda s: len(s.routes), reverse=True)

    borne_bas = 0
    pas = 2
    compagnie = None
    while True:
        borne_haut = min(len(compagnies_filtre), borne_bas + pas)
        # On affiche seulement quelques compagnies à la fois
        liste = compagnies_filtre[borne_bas:borne_haut]
        if borne_bas > 0:
            liste.append("Voir les compagnies précédentes")
        if borne_haut < len(compagnies_filtre):
            liste.append("Voir les compagnies suivantes")
        # Faire le choix
        compagnie = ihm.choisir(liste, "Choisissez une compagnie :")
        if compagnie == "Voir les compagnies suivantes":
            borne_bas = borne_haut
        elif compagnie == "Voir les compagnies précédentes":
            borne_haut = borne_bas
            borne_bas -= pas
        else:
            print(compagnie)
            break
    return compagnie
