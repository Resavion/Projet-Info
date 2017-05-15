import numpy as np
import matplotlib.pyplot as plt
from datetime import (datetime, timedelta)
from collections import defaultdict

import ihm.console as ihm
import utilitaires.earth as earth
from utilitaires.carte import (mercator, dessine_fondcarte, parametrage_carte,
                               distance_haversine, densif_geodesique, decoupe_ligne)
from utilitaires.fonctions import saisie_compagnie
from reservation.Horaire import Horaire


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
        self._coords = None

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

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, liste):
        self._coords = liste

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

    def afficher_horaires(self):
        """
        Methode qui permet d'afficher les horaires ou cette route est empruntée
        :return: None
        """

        liste_horaires = self._horaires
        liste_horaires.sort(key=lambda s: s.heure_depart)
        ihm.afficher_paginer(liste_horaires, "Liste des horaires")
        return

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
            plt.plot(xs, ys, style+'-', linewidth=largeur)

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
            plt.title('Carte de la route {}'.format(self))
            plt.show()
        return

    def calcul_prix_route(self, classe='Y'):
        """
        Methode qui permet de calculer le prix d'un billet d'avion en
        fonction de la distance parcourue
        
        :param classe: classe du billet
        :return: prix du billet
        """

        prix_sans_classe = 0
        coeff_0_500      = 0.16
        coeff_500_1000   = 0.22
        coeff_1000_2000  = 0.17
        coeff_2000_5000  = 0.06
        coeff_5000_12000 = 0.07
        # Calcule le prix en fonction des km parcourus
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
        # Augmente le prix en fonction de la classe
        prix_avec_classe = 0
        coeff_Y = 1
        coeff_P = 2
        coeff_C = 5
        coeff_F = 11
        if classe == 'Y':
            prix_avec_classe = prix_sans_classe * coeff_Y
        elif classe == 'P':
            prix_avec_classe = prix_sans_classe * coeff_P
        elif classe == 'C':
            prix_avec_classe = prix_sans_classe * coeff_C
        elif classe == 'F':
            prix_avec_classe = prix_sans_classe * coeff_F
        else:
            pass
        return prix_avec_classe

    def chercher_vols(self, jour_depart, nb_passagers, classe):
        """
        Cherche les vols d'une route pour une date et une classe donnee
        
        :param jour_depart: 
        :param nb_passagers:
        :param classe: 
        :return: 
        """

        jour_depart = jour_depart.date()
        jour_plus1 = jour_depart.replace(day=jour_depart.day+1)
        horaires = self._horaires
        horaires.sort(key=lambda s: s.heure_depart)

        vols_tout = []
        # Pour chaque horaire de la route
        for horaire in horaires:
            # On garde les vols avec places du jour demande et du jour suivant
            vols = [x for x in horaire.vols
                    if jour_depart <= x.datetime_depart.date()
                    and x.datetime_depart.date() <= jour_plus1
                    and x.places_restantes_classe(classe) > nb_passagers]
            if vols:
                vols_tout.extend(vols)

        return vols_tout

    def creer_horaire(self, compagnies):
        """
        Methode pour creer un horaire pour la route
        
        :return: 
        """

        new_hor = None
        # Saisir numero de vol
        num_vol = ihm.demander("Saisissez un numéro de vol (1 à 4 chiffres) :")
        # Si c'est un codeshare,
        choix_codeshare = ihm.choisir(
            ['Oui', 'Non'],
            "Est-ce que cet horaire est le codeshare de l'horaire "
            "d'une autre compagnie ?")
        if choix_codeshare == 'Oui':
            # alors saisir compagnie
            compagnie = saisie_compagnie(compagnies)
            cle_route = "{}{}{}".format(compagnie.id_code_iata,
                                        self._aeroport_depart.id_code_iata,
                                        self._aeroport_arrivee.id_code_iata)
            route = Route.cle_index[cle_route]
            # et choisir horaire
            hor_tri = route.horaires
            if len(hor_tri) == 0:
                ihm.afficher("Il n'y a pas d'horaire disponible !")
                return
            # On trie les routes par nombre d'horaires
            hor_tri.sort(key=lambda s: s.numero)
            hor = ihm.choisir_paginer(hor_tri, "Choisissez l'horaire :")
            ihm.afficher("Vous avez choisi l'horaire {}".format(hor))
            # Creation du nouvel horaire
            new_hor = Horaire(self, num_vol, None, None, None, None,
                              hor, None)
        # Si ce n'est pas un codeshare
        else:
            # Saisir heure de depart
            str_h_dep = ihm.demander("Saisissez l'heure de départ (HH:MM) :")
            h_dep = datetime.strptime(str_h_dep, "%H:%M").time()
            # Saisir heure d'arrivee
            str_h_arr = ihm.demander("Saisissez l'heure d'arrivée (HH:MM) :")
            h_arr = datetime.strptime(str_h_arr, "%H:%M").time()
            # Saisir duree
            str_dur = ihm.demander("Saisissez la durée (HHhMM, ex : 0h55) :")
            t = datetime.strptime(str_dur, "%Hh%M")
            dur = timedelta(hours=t.hour, minutes=t.minute)
            # Saisir la periodicite : TODO
            period = ''
            configs = self.compagnie.configs
            configs_tri = [x for x in configs
                           if x.type_avion.distance_franchissable_km > self._distance/1000]
            configs_tri.sort(key=lambda s: s.nom)
            if len(configs_tri) == 0:
                ihm.afficher("Il n'y a pas de configuration disponible !")
                return
            # Choisir la config
            conf = ihm.choisir_paginer(
                self.compagnie.configs, "Choisissez une configuration d'avion")
            # Creation du nouvel horaire
            new_hor = Horaire(
                self, num_vol, h_dep, h_arr, dur, period, None, conf)

        # Confirmer ou pas
        choix = ihm.choisir(
            ['Oui','Non'],
            "Confirmez-vous la création de l'horaire {} ?".format(new_hor))
        if choix == 'Oui':
            self._horaires.append(new_hor)
            if new_hor.horaire_operateur is not None:
                new_hor.horaire_operateur.horaires_codeshare.append(new_hor)
            ihm.afficher("L'horaire a été créé")
        else:
            ihm.afficher("L'horaire n'a pas été créé")
        return
