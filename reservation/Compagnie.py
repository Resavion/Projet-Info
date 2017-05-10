import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

import ihm.console as ihm
from utilitaires.carte import dessine_fondcarte
from utilitaires.fonctions import saisie_date


class Compagnie(object):
    def __init__(self, id_code_iata, nom, code_icao, pays, code_continent, code_pays,
                 configs=None, avions=None, routes=None):
        """
         Constructeur de la classe compagnie
        
        :param id_code_iata: identifiant de la compagnie qui correspond au code iata
        :param nom: nom de la compagnie
        :param code_icao: code icao de la compagnie
        :param pays: pays d'origine de la compagnie
        :param code_continent: code du continent
        :param code_pays: code du pays
        :param configs: liste des configs d'avions proposees par la compagnie
        :param avions: liste des avions possedes par la compagnie
        :param routes: liste des routes assurees par la compagnie
        """
        self._id_code_iata   = id_code_iata
        self._nom            = nom
        self._code_icao      = code_icao
        self._pays           = pays
        self._code_continent = code_continent
        self._code_pays      = code_pays
        if configs is None:
            configs   = []
        self._configs = configs
        if avions is None:
            avions   = []
        self._avions = avions
        if routes is None:
            routes   = []
        self._routes = routes

    @property
    def id_code_iata(self):
        return self._id_code_iata

    @property
    def nom(self):
        return self._nom

    @property
    def code_icao(self):
        return self._code_icao

    @property
    def pays(self):
        return self._pays

    @property
    def code_continent(self):
        return self._code_continent

    @property
    def code_pays(self):
        return self._code_pays

    @property
    def configs(self):
        return self._configs

    @property
    def avions(self):
        return self._avions

    @property
    def routes(self):
        return self._routes

    @property
    def nb_routes_sans_double(self):
        """
        Methode qui permet de savoir combien de route sans doublon une compagnie a 

        :return: nombre de route sans doublon
        """

        nb_routes_double = 0
        for route in self._routes:
            for terou in self._routes:
                if route.aeroport_depart.id_code_iata == terou.aeroport_arrivee.id_code_iata:
                    if route.aeroport_arrivee.id_code_iata == terou.aeroport_depart.id_code_iata:
                        nb_routes_double += 1
        nb_routes_double = nb_routes_double / 2
        nb_sans_double = len(self._routes) - nb_routes_double
        return int(nb_sans_double)

    def __str__(self):
        return "{}, {} (IATA : {}, ICAO : {})"\
            .format(self._nom, self._pays,
                    self._id_code_iata, self._code_icao)

    def afficher_infos_avions(self):
        """
        Methode qui permet d'afficher les infos des differents avions
        :return: 
        """

        ihm.afficher("Il y a {} avion(s)".format(len(self._avions)))
        ihm.afficher_paginer(self._avions, "Avions", pas=10)
        return

    def afficher_carte_avions(self, show=True, annot=True):
        """
        Methode qui permet d'afficher l'emplacement des differents avions
        :return: None
        """

        # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        if show:
            dessine_fondcarte()
        # Ajout de la carte de chaque route
        for avion in self._avions:
            avion.afficher_carte(show=False, annot=annot)
        # Affichage
        if show:
            plt.title('Carte des avions de {0:s}'.format(self._nom))
            plt.show()
        return

    def affecter_avion(self):
        """
        Methode qui permet d'affecter un avion existant à un vol
        :return: 
        """
        pass

    def afficher_configs(self):
        """
        Methode qui permet d'afficher les configs d'avion utilisees par la compagnie
        :return: 
        """
        ihm.afficher("Il y a {} configuration(s)".format(len(self._configs)))
        ihm.afficher_paginer(self._configs, "Configurations", pas=10)
        return

    def afficher_infos_routes(self):
        """
        Methode qui permet d'afficher la liste des routes de la compagnie
        :return: 
        """

        ihm.afficher("Il y a {} route(s)".format(len(self._routes)))
        ihm.afficher_paginer(self._routes, "Routes", pas=10)
        return

    def afficher_carte_routes(self, show=True, annot=True):
        """
        Methode qui permet d'afficher la carte des routes de la compagnie
        :return: None
        """

        # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        if show:
            dessine_fondcarte()
        # Ajout de la carte de chaque route
        for route in self._routes:
            route.afficher_carte(show=False, annot=annot)
        # Affichage
        if show:
            plt.title('Carte du reseau {0:s}'.format(self._nom))
            plt.show()
        return

    def ajouter_route(self):
        """
        Methode qui permet d'ajouter une route empruntée par la compagnie pour un vol
        :return: 
        """
        pass

    def suspendre_route(self):
        """
        Methode pour suspendre une route proposee par la compagnie
        :return: 
        """
        pass

    def ajouter_vols_toutes_routes(self):
        """
        Ajoute des vols entre deux dates donnees pour toutes les routes
        qui ont des horaires
        :return: 
        """

        debut = saisie_date("date de début", datetime.today())
        nb_jours = int(ihm.demander("Saisissez un nombre de jours :"))
        for route in self._routes:
            ihm.afficher(route)
            for horaire in route.horaires:
                ihm.afficher(horaire)
                horaire.creer_vols(debut=debut, nb_jours=nb_jours)
        return

    def afficher_stats(self):
        """
        Methode qui permet d'afficher les statistiques sur le nombre de passager, etc pour la compagnie
        :return: 
        """
        pass

    def chercher_route_directe(self, dep, arr, aeros_visites):
        """
        Methode qui permet de chercher une route qui relie 2 aeroports
        
        :param dep: aeroport de depart
        :param arr: aeroport d'arrivee
        :param aeros_visites: les aeroports a ne pas reparcourir
        :return: l'eventuelle route directe, les autres routes
        """

        aeros_visites.append(dep)
        # Les routes au depart de l'aeroport
        routes = [x for x in self._routes
                  if x.aeroport_depart == dep
                  and x.aeroport_arrivee not in aeros_visites]
        # La route directe
        route_directe = [x for x in routes
                         if x.aeroport_arrivee == arr]
        # Les autres routes
        routes_suiv = [x for x in routes
                       if x.aeroport_arrivee != arr]
        return route_directe, routes_suiv

    def chercher_routes_escales(self, aer_dep, aer_arr, escales_max, classe='Y'):
        """
        Methode qui permet de chercher une route qui relie 2 aeroports en fonction du nombre d'escales
        
        :param aer_dep: aeroport de depart
        :param aer_arr: aeroport d'arrivee
        :param escales_max: nombre d'escales max
        :param classe: classe du billet cherché
        :return: les routes directes, les routes avec une escale et les routes avec deux escales
        """
        aeros_visites = []
        combinaisons = []

        # On cherche la route directe
        route_directe, routes_suiv = self.chercher_route_directe(
            aer_dep, aer_arr, aeros_visites)
        if route_directe:
            combinaisons.append(route_directe)

        if escales_max == 0:
            routes_suiv = []
        # Si escale, on cherche les routes passant par 1 autre aeroport
        for route in routes_suiv:
            route_directe, routes_suiv2 = self.chercher_route_directe(
                route.aeroport_arrivee, aer_arr, aeros_visites)
            if route_directe:
                combinaisons.append([route, *route_directe])

            if escales_max == 1:
                routes_suiv2 = []
            # Si encore escale, on cherche les routes passant par 1 autre aeroport
            routes_suiv2 = [x for x in routes_suiv2
                            if not (x.aeroport_arrivee.code_pays == route.aeroport_depart.code_pays
                                    and x.aeroport_depart.code_pays != x.aeroport_arrivee.code_pays)]
            for route2 in routes_suiv2:
                route_directe, routes_suiv3 = self.chercher_route_directe(
                    route2.aeroport_arrivee, aer_arr, aeros_visites)
                if route_directe:
                    combinaisons.append([route, route2, *route_directe])

        return combinaisons

    def afficher_aeroports(self):
        """
        Methode qui permet d'afficher les aeroports en fonction du nombre de route qui leur
        sont rattachées
        :return:
        """

        liste = defaultdict(int)
        for route in self._routes:
            liste[route.aeroport_depart] += 1
            liste[route.aeroport_arrivee] += 1
        aeros = list(liste.keys())
        aeros.sort(key=lambda s: liste[s], reverse=True)
        aeros_nb_routes = []
        for aero in aeros:
            aeros_nb_routes.append("{} - {} routes".format(aero, liste[aero]))
        ihm.afficher_paginer(aeros_nb_routes, "Liste des aéroports de {}".format(self._nom))
        return



