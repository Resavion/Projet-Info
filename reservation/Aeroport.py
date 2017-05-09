from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

import ihm.console as ihm
import utilitaires.earth as earth
from utilitaires.carte import (mercator, dessine_fondcarte, parametrage_carte)


class Aeroport(object):
    """ ca sert a quoi ???????"""
    id_index = defaultdict(list)

    def __init__(self, id_code_iata, type_aero, nom, latitude_deg, longitude_deg,
                 elevation_ft, code_continent, code_pays, municipalite, code_icao,
                 fuseau, pistes=None, avions=None,
                 routes_entrantes=None, routes_sortantes=None):
        """
        Constructeur de la classe aeroport
        
        :param id_code_iata: identifiant de l'aeroport correspondant au iata code
        :param type_aero: type de l'aeroport (grand, moyen, petit)
        :param nom: nom de l'aeroport
        :param latitude_deg: la latitude de l'aeroport
        :param longitude_deg: la longitude de l'aeroport
        :param elevation_ft: l'elevation de l'aeroport
        :param code_continent: le code du continent ou se trouve l'aeroport
        :param code_pays: le code du pays ou se trouve l'aeroport
        :param municipalite: la municipalite ou se trouve l'aeroport
        :param code_icao: le code gps de l'aeroport
        :param fuseau: fuseau horaire de l'aeroport (objet timezone)
        :param pistes: liste des pistes de l'aeroport
        :param avions: avions presents sur l'aeroport
        :param routes_entrantes: routes arrivant a l'aeroport
        :param routes_sortantes: routes parant de l'aeroport
        """
        self._id_code_iata   = id_code_iata
        self._type_aero      = type_aero
        self._nom            = nom
        self._latitude_deg   = latitude_deg
        self._longitude_deg  = longitude_deg
        self._elevation_ft   = elevation_ft
        self._code_continent = code_continent
        self._code_pays      = code_pays
        self._municipalite   = municipalite
        self._code_icao      = code_icao
        self._fuseau         = fuseau
        if pistes is None:
            pistes   = []
        self._pistes = pistes
        if avions is None:
            avions   = []
        self._avions = avions
        if routes_entrantes is None:
            routes_entrantes   = []
        self._routes_entrantes = routes_entrantes
        if routes_sortantes is None:
            routes_sortantes   = []
        self._routes_sortantes = routes_sortantes
        Aeroport.id_index[id_code_iata].append(self)

    @property
    def id_code_iata(self):
        return self._id_code_iata

    @property
    def type_aero(self):
        return self._type_aero

    @property
    def nom(self):
        return self._nom

    @property
    def latitude_deg(self):
        return self._latitude_deg

    @property
    def longitude_deg(self):
        return self._longitude_deg

    @property
    def elevation_ft(self):
        return self._elevation_ft

    @property
    def code_continent(self):
        return self._code_continent

    @property
    def code_pays(self):
        return self._code_pays

    @property
    def municipalite(self):
        return self._municipalite

    @property
    def code_icao(self):
        return self._code_icao

    @property
    def fuseau(self):
        return self._fuseau

    @property
    def pistes(self):
        return self._pistes

    @property
    def avions(self):
        return self._avions

    @property
    def routes_entrantes(self):
        return self._routes_entrantes

    @property
    def routes_sortantes(self):
        return self._routes_sortantes

    @classmethod
    def find_by_id(cls, id_code_iata):
        return Aeroport.id_index[id_code_iata]

    def __str__(self):
        return "{} {}, {}, {} (IATA : {}, ICAO : {})"\
            .format(self._id_code_iata, self._nom,
                    self._municipalite, self._code_pays,
                    self._id_code_iata, self._code_icao)

    def afficher_carte(self, show=True, annot=True, routes=False):
        """
        Methode qui permet d'afficher la carte du monde avec l'aeroport en question
        
        :param show: booleen qui permet de choisir s'il faut montrer la carte ou non
        :param annot: booleen qui permet de choisir si on veut afficher les annotations ou non
        """

        # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        if show:
            dessine_fondcarte()

        # Coordonnees de l'aeroport
        list_coords = np.zeros((1, 2))
        list_coords[0, 0] = self._latitude_deg
        list_coords[0, 1] = self._longitude_deg
        # Transfo en Mercator
        xs0, ys0 = mercator(list_coords, earth.E, 0, 0, earth.A)
        # Ajout points a la carte
        plt.plot(xs0, ys0, 'b.')

        # Ajout des routes a la carte si demande
        if routes:
            for route in self._routes_sortantes:
                route.afficher_carte(show=False, annot=annot)
            for route in self._routes_entrantes:
                route.afficher_carte(show=False, annot=annot)

        # Parametrage de la carte
        parametrage_carte()

        # Ajout de tag avec le code de l'aeroport
        if annot:
            fig = plt.gcf()
            ax  = fig.add_subplot(111)
            ax.annotate('{0:s}'.format(self.id_code_iata), xy=(xs0, ys0), xytext=(4, -4), \
                        fontsize=6, textcoords='offset points')
        # Affichage
        if show:
            plt.title("Carte de l'aeroport {0:s}".format(self._nom))
            plt.show()
        return

    def afficher_routes_sortantes(self):
        """
        Affiche toutes les routes possibles qui partent de l'aeroport
        
        :return: 
        """
        ihm.afficher("Il y a {} route(s) sortante(s)"
                     .format(len(self.routes_sortantes)))
        ihm.afficher_paginer(self.routes_sortantes, "Routes sortantes", pas=10)
        return

    def afficher_routes_entrantes(self):
        """
        Affiche toutes les routes possibles qui arrivent a l'aeroport

        :return: 
        """
        ihm.afficher("Il y a {} route(s) entrante(s)"
                     .format(len(self.routes_entrantes)))
        ihm.afficher_paginer(self.routes_entrantes, "Routes entrantes", pas=10)
        return

    def afficher_horaires_arrivees(self):
        """
        Affiche tous les horaires d'arrivee a l'aeroport
        
        :return: 
        """
        hor_arr = []
        for route in self._routes_entrantes:
            hor_arr.extend(route.horaires)
        hor_arr.sort(key=lambda s: s.heure_arrivee)
        ihm.afficher("Il y a {} horaire(s) d'arrivée(s)"
                     .format(len(hor_arr)))
        ihm.afficher_paginer(hor_arr, "Horaires d'arrivées", pas=10)
        return

    def afficher_horaires_departs(self):
        """
        Affiche tous les horaires de depart l'aeroport

        :return: 
        """
        hor_arr = []
        for route in self._routes_sortantes:
            horaires = [x for x in route.horaires
                        if x.horaire_operateur is None]
            hor_arr.extend(horaires)
        hor_arr.sort(key=lambda s: s.heure_depart)
        ihm.afficher("Il y a {} horaire(s) de départ(s)"
                     .format(len(hor_arr)))
        ihm.afficher_paginer(hor_arr, "Horaires de départs", pas=10)
        return

    def afficher_avions(self):
        """
        Methode qui permet d'afficher tous les avions au sol
        
        :return: 
        """
        ihm.afficher("Il y a {} avion(s) au sol à l'aéroport"
                     .format(len(self._avions)))
        ihm.afficher_paginer(self._avions, "Avions au sol", pas=10)
        return

    def afficher_vols(self):
        """
        Methode qui permet d'afficher tous les vols d'arrivee et de depart de l'aéroport un jour donné
        
        :return: 
        """
        pass
