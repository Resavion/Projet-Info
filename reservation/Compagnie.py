import numpy as np
import matplotlib.pyplot as plt

import ihm.console as ihm
import utilitaires.earth as earth
from utilitaires.carte import mercator


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
        self._id_code_iata = id_code_iata
        self._nom = nom
        self._code_icao = code_icao
        self._pays = pays
        self._code_continent = code_continent
        self._code_pays = code_pays
        if configs is None:
            configs = []
        self._configs = configs
        if avions is None:
            avions = []
        self._avions = avions
        if routes is None:
            routes = []
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

    def afficher_carte_avions(self):
        """
        Methode qui permet d'afficher l'emplacement des differents avions
        :return: 
        """
        pass

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
            # Lecture du trait de cotes
            coords_latlon = np.genfromtxt('utilitaires/coast2.txt')
            # Transfo en Mercator
            x, y = mercator(coords_latlon, earth.E, 0, 0, earth.A)
            # Ajout a la carte
            plt.fill(x, y, 'bisque', linewidth=0.1)

        # Ajout de la carte de chaque station
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

    def afficher_stats(self):
        """
        Methode qui permet d'afficher les statistiques sur le nombre de passager, etc pour la compagnie
        :return: 
        """
        pass

    def chercher_routes(self, aer_dep, aer_arr, escales_max):
        routes_directes = []
        routes_1escale = []
        routes_2escales = []

        routes = [x for x in self.routes if x.aeroport_depart == aer_dep]
        aeroports_visites = [aer_dep]

        route_directe = [x for x in routes if x.aeroport_arrivee == aer_arr]
        if route_directe:
            routes_directes.extend(route_directe)

        if escales_max > 0:
            routes_indirectes = [x for x in routes if x.aeroport_arrivee != aer_arr]
            aeroports_visites.extend([x.aeroport_arrivee for x in routes_indirectes])

            for route_indirecte in routes_indirectes:
                routes_sortantes, route_1escale = self.routes_avec_1escale(
                    self, aeroports_visites, route_indirecte, aer_arr
                )
                if route_1escale:
                    routes_1escale.append(route_1escale)

                if escales_max > 1:
                    for route_sortante in routes_sortantes:
                        route_2escales = self.route_avec_2escales(
                            self, route_indirecte, route_sortante, aer_arr
                        )
                        if route_2escales:
                            routes_2escales.append(route_2escales)

        return routes_directes, routes_1escale, routes_2escales

    @staticmethod
    def routes_avec_1escale(compagnie, aeroports_visites, route1, aer_arr):
        escale = route1.aeroport_arrivee
        routes2 = [
            x for x in compagnie.routes
            if x.aeroport_depart == escale
            and x.aeroport_arrivee not in aeroports_visites
        ]
        route_1escale = [x for x in routes2 if x.aeroport_arrivee == aer_arr]
        if route_1escale:
            return routes2, [route1, *route_1escale]
        return routes2

    @staticmethod
    def route_avec_2escales(compagnie, route1, route2, aer_arr):
        escale = route2.aeroport_arrivee
        route_2escales = [
            x for x in compagnie.routes
            if x.aeroport_depart == escale and x.aeroport_arrivee == aer_arr
        ]
        if route_2escales:
            return [route1, route2, *route_2escales]
        return None


    def afficher_aeroports(self):
        """
        Methode qui permet d'afficher les aeroports en fonction du nombre de route qui leur
        sont rattachées
        :return:
        """
        pass



