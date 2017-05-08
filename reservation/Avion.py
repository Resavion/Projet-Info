from datetime import date

import ihm.console as ihm


class Avion(object):
    def __init__(self, id_avion, compagnie, config, aeroport, date_livraison, date_derniere_revision,
                 etat, latitude_deg=None, longitude_deg=None, vols=None):
        """
        Constructeur de la classe avion
        
        :param id_avion: identifiant avion
        :param compagnie: compagnie qui possède l'avion
        :param config: configuration de l'avion
        :param aeroport: aeroport ou il se situe actuellement
        :param date_livraison: date de livraison de l'avion
        :param date_derniere_revision: derniere date de revision de l'avion
        :param etat: donne l'etat de l'avion, si il est en vol, au sol, non utilisable
        :param latitude_deg: la latitude en degres de la position de l'avion
        :param longitude_deg: la longitude en degres de la position de l'avion
        :param vols: vols assures par l'avion
        """
        self._id = id_avion
        self._compagnie = compagnie
        self._config = config
        self._date_livraison = date_livraison
        self._date_derniere_revision = date_derniere_revision
        self._etat = etat
        self._aeroport = aeroport
        if latitude_deg is None:
            latitude_deg = aeroport.latitude_deg
        self._latitude_deg = latitude_deg
        if longitude_deg is None:
            longitude_deg = aeroport.longitude_deg
        self._longitude_deg = longitude_deg
        if vols is None:
            vols = []
        self._vols = vols

    @property
    def id(self):
        return self._id

    @property
    def compagnie(self):
        return self._compagnie

    @property
    def config(self):
        return self._config

    @property
    def date_livraison(self):
        return self._date_livraison

    @property
    def date_derniere_revision(self):
        return self._date_derniere_revision

    @property
    def etat(self):
        return self._etat

    @property
    def aeroport(self):
        return self._aeroport

    @property
    def latitude_deg(self):
        return self._latitude_deg

    @property
    def longitude_deg(self):
        return self._longitude_deg

    @property
    def vols(self):
        return self._vols

    @property
    def age(self):
        when = self._date_livraison
        on = date.today()
        was_earlier = (on.month, on.day) < (when.month, when.day)
        nb_annees = on.year - when.year - was_earlier
        dernier_anniv = date(when.year + nb_annees, when.month, when.day)
        prochain_anniv = date(when.year + nb_annees + 1, when.month, when.day)
        jours_ecoules = (on - dernier_anniv).days
        duree_annee = (prochain_anniv - dernier_anniv).days
        ratio = jours_ecoules/duree_annee
        return "{:.1f}".format(nb_annees + ratio)

    @date_derniere_revision.setter
    def date_derniere_revision(self, valeur):
        self._date_derniere_revision = valeur

    def __str__(self):
        txt = "{} - Id : {} - {} - Config {} : {}F/{}C/{}P/{}Y ({} pax) - " \
               "Age : {} ans (1er vol : {}, revision : {}) - {}"\
              .format(self._compagnie.id_code_iata, self._id,
                      self._config.type_avion, self._config.nom,
                      self._config.nb_places_premiere,
                      self._config.nb_places_business,
                      self._config.nb_places_eco_plus,
                      self._config.nb_places_eco,
                      self._config.nb_total_places,
                      self.age, self._date_livraison,
                      self._date_derniere_revision,
                      self._etat)
        if self.aeroport is not None:
            txt += " - à {}".format(self.aeroport)
        return txt

    def afficher_carte(self):
        pass

    def afficher_vols(self):
        """
        Methode qui permet d'afficher les vols assures par l'avion
        :return: 
        """
        ihm.afficher("Il y a {} vol(s)".format(len(self._vols)))
        ihm.afficher_paginer(self._vols, "Vols", pas=10)
        return

    def afficher_statistiques(self):
        pass
