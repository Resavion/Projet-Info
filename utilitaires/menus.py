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
        recherche = ihm.choisir(actions, "Choisissez un mode de recherche :")
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
                   'Gérer les routes',
                   'Afficher les statistiques',
                   'Revenir au début')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            actions_avions(compagnie)
        elif action == actions[1]:
            actions_routes(compagnie)
        elif action == actions[2]:
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
        else:  # On a choisi une compagnie
            break
    return compagnie


def choisir_par_code(compagnies):
    compagnie = None
    code = ihm.demander("Tapez le code IATA (2 caractères) "
                        "ou ICAO (3 caractères) :")
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
                   'Afficher une carte des avions',
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
    code = ihm.demander("Tapez l'identifiant de l'avion :")
    results = [x for x in compagnie.avions if x.id == code]
    if len(results) == 0:
        ihm.afficher("Désolé, nous n'avons pas trouvé votre avion !")
        return
    avion = results[0]
    ihm.afficher("Vous allez gérer l'avion {}".format(avion))
    # Proposer les actions
    while True:
        actions = ("Afficher une carte de l'avion",
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
    route = None
    code = ihm.demander("Tapez l'identifiant de la route :")
    results = [x for x in compagnie.routes if x.id == int(code)]
    if len(results) == 0:
        ihm.afficher("Désolé, nous n'avons pas trouvé votre route !")
        return
    route = results[0]
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

