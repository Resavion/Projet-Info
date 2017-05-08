from datetime import (datetime, timedelta)

import ihm.console as ihm
from utilitaires.fonctions import (saisie_date)
from reservation.Vol import Vol


class Horaire(object):
    def __init__(self, route, numero, heure_depart, heure_arrivee, duree, periodicite,
                 horaire_operateur, config_avion=None, vols=None):
        """
        Constructeur de la classe horaire
        
        :param route: route empruntee par le vol
        :param numero: numero de vol 
        :param heure_depart: heure de depart du vol
        :param heure_arrivee: heure d'arrivee du vol
        :param duree: duree du vol
        :param periodicite: nombre de fois ou ce vol est effectue (par semaine, mois, annee, saison...)
        :param horaire_operateur: horaire de la compagnie qui va operer le vol
        :param config_avion: la configuration d'avion utilisee a cet horaire
        :param vols: vols assurant cet horaire
        """
        self._route = route
        self._numero = numero
        self._heure_depart = heure_depart
        self._heure_arrivee = heure_arrivee
        self._duree = duree
        self._periodicite = periodicite
        self._horaire_operateur = horaire_operateur
        self._config_avion = config_avion
        if vols is None and horaire_operateur is None:
            vols = []
        self._vols = vols

    @property
    def route(self):
        return self._route

    @property
    def compagnie(self):
        return self._route.compagnie

    @property
    def numero(self):
        return self._numero

    @property
    def heure_depart(self):
        if self._horaire_operateur is not None:
            return self._horaire_operateur.heure_depart
        return self._heure_depart

    @property
    def heure_arrivee(self):
        if self._horaire_operateur is not None:
            return self._horaire_operateur.heure_arrivee
        return self._heure_arrivee

    @property
    def duree(self):
        if self._horaire_operateur is not None:
            return self._horaire_operateur.duree
        return self._duree

    @property
    def periodicite(self):
        if self._horaire_operateur is None:
            return self._horaire_operateur.periodicite
        return self._periodicite

    @property
    def horaire_operateur(self):
        return self._horaire_operateur

    @property
    def config_avion(self):
        if self._horaire_operateur is not None:
            return self._horaire_operateur.config_avion
        return self._config_avion

    @property
    def vols(self):
        if self._horaire_operateur is not None:
            return self._horaire_operateur.vols
        return self._vols

    def __str__(self):
        return "{} {:4s} - {} {:%H:%M} -> {} {:%H:%M} ({}h{:02d})"\
            .format(self.compagnie.id_code_iata, str(self._numero),
                    self._route.aeroport_depart.id_code_iata,
                    self.heure_depart,
                    self._route.aeroport_arrivee.id_code_iata,
                    self.heure_arrivee,
                    self.duree.seconds // 3600, (self.duree.seconds//60) % 60)

    def afficher_vols(self):
        vols_tri = self._vols
        vols_tri.sort(key=lambda s: s.datetime_depart, reverse=True)
        ihm.afficher("Il y a {} vol(s)".format(len(vols_tri)))
        ihm.afficher_paginer(vols_tri, "Vols", pas=10)


    def creer_vols(self):
        """
        Cree des vols correspondants a l'horaire entre deux dates donnees
        :return: 
        """
        debut = saisie_date("date de début", datetime.today())
        fin = saisie_date("date de fin", debut)
        roundeddebut = debut.replace(hour=0, minute=0, second=0, microsecond=0)
        roundedfin = fin.replace(hour=0, minute=0, second=0, microsecond=0)
        days = (roundedfin - roundeddebut).days
        for day in range(days+1):
            td = timedelta(days=day)
            jour = debut + td
            vol = Vol(self,)
        return

    def afficher_stats(self):
        """
        
        :return: 
        """
        pass