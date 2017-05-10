from datetime import (datetime, timedelta)
from pytz import timezone

import ihm.console as ihm
from utilitaires.fonctions import (saisie_date)
from reservation.Vol import Vol
from reservation.Enums import EnumStatutVol


class Horaire(object):
    def __init__(self, route, numero, heure_depart, heure_arrivee, duree, periodicite,
                 horaire_operateur, config_avion=None, horaires_codeshare=None,
                 vols=None):
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
        :param horaires_codeshare: horaires en partage de code sur cet horaire
        :param vols: vols assurant cet horaire
        """
        self._route             = route
        self._numero            = numero
        self._heure_depart      = heure_depart
        self._heure_arrivee     = heure_arrivee
        self._duree             = duree
        self._periodicite       = periodicite
        self._horaire_operateur = horaire_operateur
        self._config_avion      = config_avion
        if horaires_codeshare is None:
            horaires_codeshare = []
        self._horaires_codeshare = horaires_codeshare
        if vols is None and horaire_operateur is None:
            vols   = []
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
    def horaires_codeshare(self):
        return self._horaires_codeshare

    @property
    def vols(self):
        if self._horaire_operateur is not None:
            return self._horaire_operateur.vols
        return self._vols

    def __str__(self):
        txt = "{} {:4s} - {} {:%H:%M} -> {} {:%H:%M} ({}h{:02d})"\
            .format(self.compagnie.id_code_iata, str(self._numero),
                    self._route.aeroport_depart.id_code_iata,
                    self.heure_depart,
                    self._route.aeroport_arrivee.id_code_iata,
                    self.heure_arrivee,
                    self.duree.seconds // 3600, (self.duree.seconds//60) % 60)
        if self._horaires_codeshare:
            txt += " - En partage de codes : "
            liste_num = []
            for hor in self._horaires_codeshare:
                liste_num.append("{} {}".format(hor.compagnie.id_code_iata,
                                                hor.numero))
            txt += ", ".join(liste_num)
        return txt

    def afficher_vols(self):
        """
        Methode qui permet d'afficher les vols disponibles
        
        :return: None
        """

        vols_tri = self._vols
        vols_tri.sort(key=lambda s: s.datetime_depart, reverse=True)
        ihm.afficher("Il y a {} vol(s)".format(len(vols_tri)))
        ihm.afficher_paginer(vols_tri, "Vols", pas=10)
        return

    def creer_vols(self,debut=None,nb_jours=None):
        """
        Methode qui permet de creer des vols correspondants a l'horaire entre deux dates donnees

        :param debut: date de debut
        :param nb_jours: nombres de jours pour lesquels on veut creer des vols apres la date de debut
        :return:
        """

        if debut is None:
            debut = saisie_date("date de début", datetime.today())
        if nb_jours is None:
            nb_jours = int(ihm.demander("Saisissez un nombre de jours :"))
        for day in range(nb_jours):
            td = timedelta(days=day)
            jour = debut + td
            vol_deb = jour.replace(hour=self.heure_depart.hour,minute=self.heure_depart.minute)
            deb_tz = self.route.aeroport_depart.fuseau
            # On ajoute la timezone de depart
            vol_deb = deb_tz.localize(vol_deb)
            # On calcule la datetime d'arrivee dans la timezone de depart
            vol_fin = deb_tz.normalize(vol_deb + self.duree)
            # On transforme dans la timezone d'arrivee
            vol_fin = vol_fin.astimezone(self.route.aeroport_arrivee.fuseau)
            # On renleve l'information de timezeone
            vol_deb = vol_deb.replace(tzinfo=None)
            vol_fin = vol_fin.replace(tzinfo=None)
            # Creation de l'objet vol
            cle = "{}{}{}".format(self.compagnie.id_code_iata,
                                  self.numero,vol_deb)
            if cle not in Vol.cle_index:
                vol = Vol(self,vol_deb,vol_fin,self.duree,None,
                          self.config_avion.nb_places_premiere,
                          self.config_avion.nb_places_business,
                          self.config_avion.nb_places_eco_plus,
                          self.config_avion.nb_places_eco,
                          EnumStatutVol(1))
                self.vols.append(vol)
                print(vol)
            else:
                print("Ce vol existe déjà")
        return
