from datetime import datetime

import ihm.console as ihm
from reservation.Client import Client


def actions_client(clients, compagnies, aeroports):
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
        actions = ('Faire une réservation', 'Consulter ses réservations',
                   'Modifier une réservation', 'Annuler une réservation',
                   'Revenir au début')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            client.faire_reservation(compagnies, aeroports)
        elif action == actions[1]:
            client.consulter_reservations()
        elif action == actions[2]:
            client.modifier_reservation()
        elif action == actions[3]:
            client.annuler_reservation()
        else:
            break
    return


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
                   "Gérer les configurations d'avion",
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

    compagnie = ihm.choisir_paginer(
        compagnies_filtre, "Choisissez une compagnie :", pas=10)
    return compagnie


def choisir_par_code(compagnies):
    compagnie = None
    code = ihm.demander(
        "Tapez le code IATA (2 caractères) ou ICAO (3 caractères) :")
    results = [x for x in compagnies
               if x.id_code_iata == code or x.code_icao == code]
    if len(results) == 0:
        ihm.afficher("Désolé, nous n'avons pas trouvé votre compagnie !")
    elif len(results) > 1:
        compagnie = ihm.choisir(results, "Précisez votre choix :")
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
                   'Ajouter un avion',
                   'Retirer un avion',
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            compagnie.afficher_infos_avions()
        elif action == actions[1]:
            compagnie.afficher_carte_avions()
        elif action == actions[2]:
            gerer_avion(compagnie)
        elif action == actions[3]:
            compagnie.ajouter_avion()
        elif action == actions[4]:
            compagnie.retirer_avion()
        else:
            break
    return


def gerer_avion(compagnie):
    avion = None
    avions = compagnie.avions
    avions.sort(key=lambda s: s.id, reverse=True)
    avion = ihm.choisir_paginer(avions, "Choisissez un avion :")
    ihm.afficher("Vous allez gérer l'avion {}".format(avion))
    # Proposer les actions
    while True:
        actions = ("Afficher une carte de la position de l'avion",
                   "Afficher les vols de l'avion",
                   "Afficher les statistiques",
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            avion.afficher_carte()
        elif action == actions[1]:
            avion.afficher_vols()
        elif action == actions[2]:
            avion.afficher_statistiques()
        else:
            break
    return


def actions_routes(compagnie):
    # Proposer les actions
    while True:
        actions = ('Afficher la liste des routes',
                   'Afficher une carte des routes',
                   'Gérer une route',
                   'Ajouter une route',
                   'Suspendre une route',
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            compagnie.afficher_infos_routes()
        elif action == actions[1]:
            compagnie.afficher_carte_routes()
        elif action == actions[2]:
            gerer_route(compagnie)
        elif action == actions[3]:
            compagnie.ajouter_route()
        elif action == actions[4]:
            compagnie.suspendre_route()
        else:
            break
    return


def gerer_route(compagnie):
    route = ihm.choisir_paginer(compagnie.routes, "Choisissez la route :")
    ihm.afficher("Vous allez gérer la route {}".format(route))
    # Proposer les actions
    while True:
        actions = ("Afficher une carte de la route",
                   "Afficher les horaires de la route",
                   "Gérer un horaire",
                   "Afficher les statistiques",
                   'Revenir au menu précédent')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            route.afficher_carte()
        elif action == actions[1]:
            route.afficher_horaires()
        elif action == actions[2]:
            pass
        elif action == actions[3]:
            route.afficher_statistiques()
        else:
            break
    return

def actions_visualisation(compagnies,aeroports):
    # Proposer les actions
    while True:
        actions = ('Gérer un aéroport',
                   'Afficher la carte de tous les aéroports',
                   'Afficher la carte de toutes les routes')

        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            choisir_par_code_aeroport(aeroports)
            # aeroports.choisir_par_code_aeroport()
        elif action == actions[1]:
            afficher_carte_aeroports(aeroports)
            # aeroports.afficher_carte_aeroports()
        elif action == action[2]:
            afficher_carte_routes(compagnies)
            # compagnies.afficher_carte_routes()
        else:
            break
    return

def choisir_par_code_aeroport(aeroports):
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
    :return:
    """

    # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
    if show:
        # Lecture du trait de cotes
        coords_latlon = np.genfromtxt('utilitaires/coast.txt')
        # Transfo en Mercator
        x, y = mercator(coords_latlon, earth.E, 0, 0, 6378137.0)
        # Ajout a la carte
        plt.fill(x, y, 'bisque', linewidth=0.1)

    # Ajout de la carte de chaque station
    for aeroport in aeroports:
        aeroport.afficher_carte(show=False, annot=False)

    # Affichage
    if show:
        plt.title('Carte de toutes les aéroports')
        plt.show()


def afficher_carte_routes(compagnies, show=True):
    """
    Methode qui permet d'afficher la carte des routes de la compagnie
    :return:
    """

    # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
    if show:
        # Lecture du trait de cotes
        coords_latlon = np.genfromtxt('utilitaires/coast.txt')
        # Transfo en Mercator
        x, y = mercator(coords_latlon, earth.E, 0, 0, 6378137.0)
        # Ajout a la carte
        plt.fill(x, y, 'bisque', linewidth=0.1)

    # Ajout de la carte de chaque station
    for compagnie in compagnies:
        compagnie.afficher_carte_routes(show=False, annot=False)

    # Affichage
    if show:
        plt.title('Carte de toutes les routes')
        plt.show()

 def nb_routes_sans_double(compagnie):
    """
    Methode qui permet de savoir combien de route sans doublon une compagnie a 
    :param compagnie: 
    :return: 
    """
    nb_routes_double = 0
    for route in compagnie.routes:
        for terou in compagnie.routes:
            if route.aeroport_depart.id_code_iata == terou.aeroport_arrivee.id_code_iata:
                if route.aeroport_arrivee.id_code_iata == terou.aeroport_depart.id_code_iata:
                    nb_routes_double += 1
    nb_routes_double = nb_routes_double / 2
    nb_routes_sans_double = len(compagnie.routes) - nb_routes_double
    return(nb_routes_sans_double)

def ranger_liste_aeroport(compagnies):
    liste_a_trier = []
    for compagnie in compagnies:
        nb_route = nb_routes_sans_double(compagnie)
        liste_a_trier.append((compagnie, nb_route))
    nb_aeroport = len(liste_a_trier)
    if nb_aeroport <= 1:
        print(liste_a_trier)
    for i in range(nb_aeroport):
        for j in range(nb_aeroport):
            if liste_a_trier[i][1] >= liste_a_trier[j][1]:
                stock = liste_a_trier[i]
                liste_a_trier[i] = liste_a_trier[j]
                liste_a_trier[j] = stock

    return(liste_a_trier)