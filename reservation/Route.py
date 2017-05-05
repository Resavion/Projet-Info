import math as ma
import numpy as np
import matplotlib.pyplot as plt

import ihm.console as ihm
import utilitaires.earth as earth
from utilitaires.carte import (mercator, add_arrow, distance_haversine,
                               densif_geodesique, decoupe_ligne)


class Route(object):
    def __init__(self, id_route, compagnie, aeroport_depart, aeroport_arrivee, geom, codeshare,
                 horaires=None):
        """
        Constructeur de la classe route
        
        :param id_route: id de la route
        :param compagnie: compagnie qui propose la route
        :param aeroport_depart: aeroport de depart de la route
        :param aeroport_arrivee: aeroport d'arrivee de la route
        :param geom: linestring entre les deux aeroports en WKT
        :param codeshare: booleen qui permet de savoir si un avion est partage par plusieurs compagnies
        :param horaires: liste des horaires sur cette route
        """
        self._id = id_route
        self._compagnie = compagnie
        self._aeroport_depart = aeroport_depart
        self._aeroport_arrivee = aeroport_arrivee
        self._geom = geom
        self._distance = distance_haversine(aeroport_depart.latitude_deg,
                                            aeroport_depart.longitude_deg,
                                            aeroport_arrivee.latitude_deg,
                                            aeroport_arrivee.longitude_deg)
        self._codeshare = codeshare
        if horaires is None:
            horaires = []
        self._horaires = horaires

    @property
    def id(self):
        return self._id

    @property
    def compagnie(self):
        return self._compagnie

    @property
    def aeroport_depart(self):
        return self._aeroport_depart

    @property
    def aeroport_arrivee(self):
        return self._aeroport_arrivee

    @property
    def geom(self):
        return self._geom

    @property
    def codeshare(self):
        return self._codeshare

    @property
    def distance(self):
        return self._distance

    @property
    def horaires(self):
        return self._horaires

    def __str__(self):
        return "{} - Id : {} - {} ({},{}) -> {} ({},{}) - {:.0f} km - " \
               "Horaires : {}"\
            .format(self._compagnie.id_code_iata,
                    self._id,
                    self._aeroport_depart.id_code_iata,
                    self._aeroport_depart.municipalite,
                    self._aeroport_depart.code_pays,
                    self._aeroport_arrivee.id_code_iata,
                    self._aeroport_arrivee.municipalite,
                    self._aeroport_arrivee.code_pays,
                    self._distance / 1000,
                    len(self._horaires))

    def ajouter_horaire(self):
        """
        Methode qui permet d'ajouter un horaire de vol a une route 
        :return: 
        """
        pass

    def supprimer_horaire(self):
        """
        Methode qui permet de supprimer un horaire de vol a une route
        
        :return: 
        """
        pass

    def calculer_plan_vol(self):
        """
        Methode pour calculer le trajet de l'avion en fonction des zones autorisées
        :return: 
        """
        pass

    def afficher_stats(self):
        """
        Methode qui permet d'afficher les statistiques sur le nombre de personnes ayant réellement
        emprunté le chemin par rapport au nombre de places offertes
        :return: 
        """
        pass

    def afficher_horaires(self):
        """
        Methode qui permet d'afficher les horaires ou cette route est empruntée
        :return: 
        """
        for horaire in self._horaires:
            print(horaire)
        ihm.demander("Tapez sur une touche pour revenir au menu")
        return

    def chercher_horaire(self, date):
        pass

    def afficher_plan_vol(self):
        """
        Methode qui permet d'afficher le plan de vol et les différents points de passages (????)
        de l'avion
        :return: 
        """
        pass

    def afficher_carte(self, start=None, show=True, annot=True):
        """
        Methode qui permet d'afficher la route reliant deux aeroports
        :return: 
        """

        # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        if show:
            # Lecture du trait de cotes
            coords_latlon = np.genfromtxt('utilitaires/coast.txt', delimiter=" ")
            # Transfo en Mercator
            x, y = mercator(coords_latlon, earth.E, 0, 0, earth.A)
            # Ajout a la carte
            plt.fill(x, y, 'bisque', linewidth=0.1)

        # Coordonnees de la route
        list_coords = np.zeros((2, 2))
        list_coords[0, 0] = self._aeroport_depart.latitude_deg
        list_coords[0, 1] = self._aeroport_depart.longitude_deg
        list_coords[1, 0] = self._aeroport_arrivee.latitude_deg
        list_coords[1, 1] = self._aeroport_arrivee.longitude_deg
        # Transfo en Mercator
        xs0, ys0 = mercator(list_coords, earth.E, 0, 0, earth.A)
        # Ajout points a la carte
        plt.plot(xs0, ys0, 'b.')

        # Densification suivant la ligne geodesique
        new_coords = densif_geodesique(list_coords, self._distance)
        tab_listes = decoupe_ligne(new_coords)
        for coords in tab_listes:
            # Transfo en Mercator
            xs, ys = mercator(coords, earth.E, 0, 0, earth.A)
            # Ajout a la carte
            style = 'b'
            if self._codeshare:
                style = 'c'
            largeur = 0.1
            if show:
                largeur = 0.5
            ligne = plt.plot(xs, ys, style+'-', linewidth=largeur)[0]
            # add_arrow(ligne)

        # Parametrage de la carte
        plt.axis([-1200000000.0, 1250000000.0, -1100000000.0, 1800000000.0])
        plt.tick_params(axis='both', which='both', bottom='off', top='off', \
                        right='off', left='off')
        frame1 = plt.gca()
        frame1.axes.xaxis.set_ticklabels([])
        frame1.axes.yaxis.set_ticklabels([])
        frame1.set_axis_bgcolor('lightcyan')

        # Ajout de tags avec les codes des aeroports
        if annot:
            fig = plt.gcf()
            ax = fig.add_subplot(111)
            for X, Y, T in zip(xs0, ys0, [self._aeroport_depart.id_code_iata,
                                          self._aeroport_arrivee.id_code_iata]):
                ax.annotate('{0:s}'.format(T), xy=(X, Y), xytext=(4, -4), \
                            fontsize=10, textcoords='offset points')

        # Affichage
        if show:
            # plt.title('Carte de la station {0:s}'.format(self.code))
            plt.show()
        return
