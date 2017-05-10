from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

import ihm.console as ihm
import utilitaires.earth as earth
from utilitaires.carte import (mercator, dessine_fondcarte, densif_geodesique,
                               decoupe_ligne, parametrage_carte)
from reservation.Client import Client


def menu_racine(clients, compagnies, aeroports):
    """
    Methode qui permet de choisir la façon dont on veut interagir avec l'interface
    
    :param clients: liste des clients
    :param compagnies: liste des compagnies
    :param aeroports: liste des aeroports
    :return: None
    """

    while True:
        # Choisir un mode d'utilisation
        modes = ('Client', 'Compagnie', 'Visualisation seule', 'Quitter')
        choix = ihm.choisir(modes, "Choisissez un mode d'utilisation :")

        # Si Client
        if choix == modes[0]:
            actions_client(clients, compagnies, aeroports)
        # Si Compagnie
        elif choix == modes[1]:
            actions_compagnie(compagnies)
        # Si Visualisation
        elif choix == modes[2]:
            actions_visualisation(compagnies, aeroports)
        # Sinon on veut quitter le programme
        else:
            break
    ihm.afficher("Vous quittez le programme.")
    return


def actions_client(clients, compagnies, aeroports):
    """
    Methode qui permet de laisser le client choisir les actions qu'ils souhaitent réaliser
    
    :param clients: liste des clients
    :param compagnies: liste des compagnies
    :param aeroports: liste des aeroports
    :return: None
    """

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

    while True:
        # Demander action : Faire, Consulter, Modifier, Annuler
        actions = ('Consulter ses réservations',
                   'Gérer une réservation',
                   'Faire une réservation',
                   'Revenir au début')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            client.consulter_reservations()
        elif action == actions[1]:
            gerer_reservation(client)
        elif action == actions[2]:
            client.faire_reservation(compagnies, aeroports)
        else:
            break
    return


def gerer_reservation(client):
    """
    Methode qui permet au client de gerer sa reservation
    
    :param client: objet client
    :return: 
    """

    # Choisir une reservation
    resas_tri = client.reservations
    resas_tri.sort(key=lambda s: s.date_achat, reverse=True)
    resa = ihm.choisir_paginer(
        resas_tri, "Choisir la réservation à afficher :")
    ihm.afficher("Vous avez choisi la réservation {}".format(resa))

    while True:
        # Demander action : Faire, Consulter, Modifier, Annuler
        actions = ('Afficher le récapitulatif',
                   'Revenir au début')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            resa.fournir_recapitulatif()
        else:
            break
    return


def ajouter_client(clients):
    """
    Methode qui permet de creer un nouveau client
    
    :param clients: liste des clients existants
    :return: nouveau client
    """

    new_id = 1
    if len(clients) != 0:
        new_id = clients[-1].id + 1
    nom = ihm.demander("Saisissez votre nom :")
    prenom = ihm.demander("Saisissez votre prénom :")
    date_naiss = None
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
    """
     Methode qui permet a la compagnie de choisir les actions qu'elle souhaite réaliser
     
    :param compagnies: liste des compagnies
    :return: ??
    """

    compagnie = None
    while compagnie is None:
        # On demande comment choisir une compagnie
        actions = ('Recherche par continent',
                   'Recherche par code IATA ou ICAO',
                   'Revenir au début')
        recherche = ihm.choisir(
            actions, "Choisissez un mode de recherche de la compagnie :")
        # Si recherche par continents
        if recherche == actions[0]:
            compagnie = choisir_par_continent(compagnies)
        # Si recherche par code
        elif recherche == actions[1]:
            compagnie = choisir_par_code(compagnies)
        # Sinon on revient au début
        else:
            return recherche

    # Proposer les actions
    while True:
        actions = ('Gérer les avions',
                   "Afficher les configurations d'avion",
                   'Gérer les routes',
                   'Afficher les statistiques',
                   'Revenir au début')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            actions_avions(compagnie)
        elif action == actions[1]:
            compagnie.afficher_configs()
        elif action == actions[2]:
            actions_routes(compagnie)
        elif action == actions[3]:
            compagnie.afficher_stats()
        else:
            break
    return


def choisir_par_continent(compagnies):
    """
    Methode qui permet de choisir une compagnie en fonction du continent
    
    :param compagnies: liste des compagnies
    :return: 
    """

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

    # On trie les compagnies par nombre de routes
    compagnies_filtre.sort(key=lambda s: len(s.routes), reverse=True)

    # Choix dans une liste paginee
    compagnie = ihm.choisir_paginer(
        compagnies_filtre, "Choisissez une compagnie :", pas=10)
    ihm.afficher("Vous allez gérer la compagnie {}".format(compagnie))
    return compagnie


def choisir_par_code(compagnies):
    """
    Methode qui permet de choisir une compagnie par ses différents codes
    
    :param compagnies: liste des compagnies
    :return: la comapgnie choisie
    """

    compagnie = None
    code = ihm.demander(
        "Tapez le code IATA (2 caractères) ou ICAO (3 caractères) :")
    results = [x for x in compagnies
               if x.id_code_iata == code or x.code_icao == code]
    if len(results) == 0:
        ihm.afficher("Désolé, nous n'avons pas trouvé votre compagnie !")
    else:
        compagnie = results[0]
    if compagnie is not None:
        ihm.afficher("Vous allez gérer la compagnie {}".format(compagnie))
    return compagnie


def actions_avions(compagnie):
    # Proposer les actions
    while True:
        actions = ('Afficher la liste des avions',
                   'Afficher une carte de la position des avions',
                   'Gérer un avion',
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            compagnie.afficher_infos_avions()
        elif action == actions[1]:
            compagnie.afficher_carte_avions()
        elif action == actions[2]:
            gerer_avion(compagnie)
        else:
            break
    return


def gerer_avion(compagnie):
    """
    Methode qui permet a la compagnie de gerer un avion
    
    :param compagnie: l'objet compagnie en question
    :return: None
    """

    avions = compagnie.avions
    avions.sort(key=lambda s: s.id, reverse=True)
    avion = ihm.choisir_paginer(avions, "Choisissez un avion :")
    ihm.afficher("Vous allez gérer l'avion {}".format(avion))
    # Proposer les actions
    while True:
        actions = ("Afficher une carte de la position de l'avion",
                   "Afficher les vols de l'avion",
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            avion.afficher_carte()
        elif action == actions[1]:
            avion.afficher_vols()
        else:
            break
    return


def actions_routes(compagnie):
    """
     Methode qui permet a la compagnie de choisir les actions qu'ils souhaitent réaliser sur une route

    :param compagnie: objet compagnie
    :return: None
    """

    # Proposer les actions
    while True:
        actions = ('Afficher la liste des routes',
                   'Afficher une carte des routes',
                   'Gérer une route',
                   'Ajouter des vols pour toutes les routes',
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            compagnie.afficher_infos_routes()
        elif action == actions[1]:
            compagnie.afficher_carte_routes()
        elif action == actions[2]:
            gerer_route(compagnie)
        elif action == actions[3]:
            compagnie.ajouter_vols_toutes_routes()
        else:
            break
    return


def gerer_route(compagnie):
    """
    Methode qui permet a la compagnie de gerer une route
    
    :param compagnie: objet compagnie
    :return: None
    """

    routes_tri = compagnie.routes
    # On trie les routes par nombre d'horaires
    routes_tri.sort(key=lambda s: len(s.horaires), reverse=True)
    route = ihm.choisir_paginer(routes_tri, "Choisissez la route :")
    ihm.afficher("Vous allez gérer la route {}".format(route))
    # Proposer les actions
    while True:
        actions = ("Afficher une carte de la route",
                   "Afficher les horaires de la route",
                   "Gérer un horaire",
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            route.afficher_carte()
        elif action == actions[1]:
            route.afficher_horaires()
        elif action == actions[2]:
            gerer_horaire(route)
        else:
            break
    return


def gerer_horaire(route):
    """
    Methode qui permet a la compagnie de gerer un horaire sur une route en question
    
    :param route: objet route
    :return: None
    """

    hor_tri = route.horaires
    # On trie les routes par nombre d'horaires
    hor_tri.sort(key=lambda s: s.numero)
    hor = ihm.choisir_paginer(hor_tri, "Choisissez l'horaire :")
    ihm.afficher("Vous allez gérer l'horaire {}".format(hor))
    # Proposer les actions
    while True:
        actions = (
            "Afficher les vols",
            "Ajouter des vols",
            'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            hor.afficher_vols()
        elif action == actions[1]:
            hor.creer_vols()
        else:
            break
    return


def actions_visualisation(compagnies,aeroports):
    """
     Methode qui permet a la compagnie de choisir les actions qu'elle souhaite réaliser pour la visualisation
     
    :param compagnies: liste des comapgnies
    :param aeroports: liste des aeroports
    :return: None
    """

    # Proposer les actions
    while True:
        actions = ('Gérer un aéroport',
                   'Afficher la carte de tous les aéroports',
                   'Afficher la carte de toutes les routes',
                   'Revenir au menu précédent')

        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            gerer_aeroport(aeroports)
        elif action == actions[1]:
            afficher_carte_aeroports(aeroports)
        elif action == actions[2]:
            afficher_carte_routes(compagnies)
        else:
            break
    return


def gerer_aeroport(aeroports):
    aero = choisir_par_code_aeroport(aeroports)
    # Proposer les actions
    while True:
        actions = (
            "Afficher la liste des routes entrantes",
            "Afficher la liste des routes sortantes",
            "Afficher la carte des routes",
            "Afficher les horaires arrivant",
            "Afficher les horaires partant",
            "Afficher la liste des avions au sol",
            'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            aero.afficher_routes_entrantes()
        elif action == actions[1]:
            aero.afficher_routes_sortantes()
        elif action == actions[2]:
            aero.afficher_carte(routes=True)
        elif action == actions[3]:
            aero.afficher_horaires_arrivees()
        elif action == actions[4]:
            aero.afficher_horaires_departs()
        elif action == actions[5]:
            aero.afficher_avions()
        else:
            break
    return


def choisir_par_code_aeroport(aeroports):
    """
    Methode qui permet de choisir un aeroport en fonction de ses codes 
    
    :param aeroports: liste aeroports
    :return: l'aeroport choisi
    """

    aeroport = None
    code = ihm.demander(
        "Tapez le code IATA (2 caractères) ou ICAO (3 caractères) :")
    results = [x for x in aeroports
               if x.id_code_iata == code or x.code_icao == code]
    if len(results) == 0:
        ihm.afficher("Désolé, nous n'avons pas trouvé votre aéroport !")
    elif len(results) > 1:
        aeroport = ihm.choisir(results, "Précisez votre choix :")
    else:
        aeroport = results[0]
    if aeroport is not None:
        ihm.afficher("Vous allez gérer l'aéroport {}".format(aeroport))
    return aeroport


def afficher_carte_aeroports(aeroports, show=True):
    """
    Methode qui permet d'afficher la carte des routes de la compagnie
    
    :param aeroports: liste des aeroports
    :param show: booleen qui permet de dire si l'on veut montrer la carte ou non
    :return: None
    """

    # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
    if show:
        dessine_fondcarte()
    # Ajout de la carte de chaque aeroport
    for aeroport in aeroports:
        aeroport.afficher_carte(show=False, annot=False)
    # Affichage
    if show:
        plt.title('Carte de toutes les aéroports')
        plt.show()
    return


def afficher_carte_routes(compagnies):
    """
    Methode qui permet d'afficher la carte des routes de la compagnie
    
    :param compagnies: liste compagnies
    :return: None
    """

    # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
    dessine_fondcarte()

    # Ajout de la carte de chaque route
    routes_parcourues = {}
    for compagnie in compagnies:
        print("Préparation des routes de {} - Liaisons : {:0d}..."
              .format(compagnie, compagnie.nb_routes_sans_double))
        for route in compagnie.routes:
            cle1 = "{}{}".format(route.aeroport_depart.id_code_iata,
                                 route.aeroport_arrivee.id_code_iata)
            cle2 = "{}{}".format(route.aeroport_arrivee.id_code_iata,
                                 route.aeroport_depart.id_code_iata)
            if cle1 not in routes_parcourues and cle2 not in routes_parcourues:
                routes_parcourues[cle1] = 1
                routes_parcourues[cle2] = 1
                list_coords = np.zeros((2, 2))
                list_coords[0, 0] = route.aeroport_depart.latitude_deg
                list_coords[0, 1] = route.aeroport_depart.longitude_deg
                list_coords[1, 0] = route.aeroport_arrivee.latitude_deg
                list_coords[1, 1] = route.aeroport_arrivee.longitude_deg
                domestique = (route.aeroport_depart.code_pays ==
                              route.aeroport_arrivee.code_pays)
                tab_listes = route.coords
                if tab_listes is None:
                    # Densification suivant la ligne geodesique
                    new_coords = densif_geodesique(list_coords, route.distance)
                    tab_listes = decoupe_ligne(new_coords)
                    route.coords = tab_listes
                # Pour chaque partie de la route, on ajoute a la carte
                for coords in tab_listes:
                    # Transfo en Mercator
                    xs, ys = mercator(coords, earth.E, 0, 0, earth.A)
                    # Ajout a la carte
                    coul = 'b'
                    if route.codeshare:
                        coul = 'c'
                    largeur = 0.2
                    if domestique:
                        largeur = 0.1
                    plt.plot(xs, ys, linestyle='-', color=coul, linewidth=largeur)

    # Parametrage de la carte
    parametrage_carte()
    # Affichage
    plt.title('Carte de toutes les routes')
    plt.show()
    return
