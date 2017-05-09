import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

import ihm.console as ihm
import utilitaires.earth as earth
from utilitaires.carte import (mercator, dessine_fondcarte, parametrage_carte,
                               distance_haversine, densif_geodesique, decoupe_ligne)


class Route(object):
    cle_index = defaultdict()

    def __init__(self, compagnie, aeroport_depart, aeroport_arrivee, geom, codeshare,
                 horaires=None):
        """
        Constructeur de la classe route
        
        :param compagnie: compagnie qui propose la route
        :param aeroport_depart: aeroport de depart de la route
        :param aeroport_arrivee: aeroport d'arrivee de la route
        :param geom: linestring entre les deux aeroports en WKT
        :param codeshare: booleen qui permet de savoir si un avion est partage par plusieurs compagnies
        :param horaires: liste des horaires sur cette route
        """
        self._compagnie        = compagnie
        self._aeroport_depart  = aeroport_depart
        self._aeroport_arrivee = aeroport_arrivee
        self._geom             = geom
        self._distance         = distance_haversine(aeroport_depart.latitude_deg,
                                                    aeroport_depart.longitude_deg,
                                                    aeroport_arrivee.latitude_deg,
                                                    aeroport_arrivee.longitude_deg)
        self._codeshare = codeshare
        if horaires is None:
            horaires   = []
        self._horaires = horaires

        cle = "{}{}{}".format(compagnie.id_code_iata,
                              aeroport_depart.id_code_iata,
                              aeroport_arrivee.id_code_iata)
        Route.cle_index[cle] = self

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
        return "{} - {} ({},{}) -> {} ({},{}) - {:.0f} km - " \
               "Horaires : {}"\
            .format(self._compagnie.id_code_iata,
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
        :return: None
        """

        liste_horaires = self._horaires
        liste_horaires.sort(key=lambda s: s.heure_depart)
        ihm.afficher_paginer(liste_horaires, "Liste des horaires")
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

    def afficher_carte(self, show=True, annot=True):
        """
        Methode qui permet d'afficher la route reliant deux aeroports
        
        :param show: booleen qui permet de choisir s'il faut montrer la carte ou non
        :param annot: booleen qui permet de choisir si on veut afficher les annotations ou non
        :return: 
        """

        # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        if show:
            dessine_fondcarte()

        # Coordonnees de la route
        list_coords = np.zeros((2, 2))
        list_coords[0, 0] = self._aeroport_depart.latitude_deg
        list_coords[0, 1] = self._aeroport_depart.longitude_deg
        list_coords[1, 0] = self._aeroport_arrivee.latitude_deg
        list_coords[1, 1] = self._aeroport_arrivee.longitude_deg
        # Transfo en Mercator
        xs0, ys0 = mercator(list_coords, earth.E, 0, 0, earth.A)
        # Ajout points a la carte
        plt.plot(xs0, ys0, 'b,')

        # Densification suivant la ligne geodesique
        new_coords = densif_geodesique(list_coords, self._distance)
        tab_listes = decoupe_ligne(new_coords)
        # Pour chaque partie de la route, on ajoute a la carte
        for coords in tab_listes:
            # Transfo en Mercator
            xs, ys = mercator(coords, earth.E, 0, 0, earth.A)
            # Ajout a la carte
            style  = 'b'
            if self._codeshare:
                style = 'c'
            largeur = 0.2
            if show:
                largeur = 0.5
            plt.plot(xs, ys, style+'-', linewidth=largeur)[0]

        # Parametrage de la carte
        parametrage_carte()

        # Ajout de tags avec les codes des aeroports
        if annot:
            fig = plt.gcf()
            ax = fig.add_subplot(111)
            for X, Y, T in zip(xs0, ys0, [self._aeroport_depart.id_code_iata,
                                          self._aeroport_arrivee.id_code_iata]):
                ax.annotate('{0:s}'.format(T), xy=(X, Y), xytext=(4, -4), \
                            fontsize=6, textcoords='offset points')

        # Affichage
        if show:
            # plt.title('Carte de la station {0:s}'.format(self.code))
            plt.show()
        return

    def calcul_prix_route(self):
        """
        Methode qui permet de calculer le prix d'un billet d'avion en
        fonction de la distance parcourue
        :return: prix du billet
        """

        prix_sans_classe = 0
        coeff_0_500      = 0.16
        coeff_500_1000   = 0.22
        coeff_1000_2000  = 0.17
        coeff_2000_5000  = 0.06
        coeff_5000_12000 = 0.07
        # Calcul le prix en fonction des km parcourus
        if self.distance < 500:
            prix_sans_classe = 60 + coeff_0_500*self._distance/1000
        elif self.distance < 1000:
            prix_sans_classe = 140 + coeff_500_1000*(self._distance/1000-500)
        elif self.distance < 2000:
            prix_sans_classe = 250 + coeff_1000_2000*(self._distance/1000-1000)
        elif self.distance < 5000:
            prix_sans_classe = 420 + coeff_2000_5000*(self._distance/1000-2000)
        elif self.distance >= 5000:
            prix_sans_classe = 600 + coeff_5000_12000*(self._distance/1000-5000)
        return prix_sans_classe
