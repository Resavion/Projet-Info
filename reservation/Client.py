from datetime import (datetime, timedelta)

import ihm.console as ihm
from utilitaires.fonctions import (saisie_date,
                                   saisie_aeroport)


class Client(object):
    def __init__(self, id_client, nom, prenom, date_naissance,
                 reservations=None):
        """
        Constructeur de la classe client
        
        :param id_client: identifiant du compte client 
        :param nom: nom du client
        :param prenom: prenom du client
        :param date_naissance: date de naissance du client
        :param reservations: liste des reservations du client
        """
        self._id             = id_client
        self._nom            = nom
        self._prenom         = prenom
        self._date_naissance = date_naissance
        if reservations is None:
            reservations   = []
        self._reservations = reservations

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def date_naissance(self):
        return self._date_naissance

    @property
    def reservations(self):
        return self._reservations

    def __str__(self):
        return "{}, {} ({:%d/%m/%Y})"\
            .format(self._nom, self._prenom, self._date_naissance)

    def faire_reservation(self, compagnies, aeroports):
        """
        Methode qui consiste a faire une reservation
        (saisir_critere, afficher_vols, choisir_vols, saisir_passager, payer..)
        
        :param compagnies: listes de compagnies
        :param aeroports: listes des aeroports
        :return: None
        """

        # Saisie des criteres
        criteres         = self.saisie_criteres(aeroports)

        routes_directes  = []
        routes_1escale   = []
        routes_2escales  = []
        aer_dep, aer_arr = criteres[:2]
        escales_max      = criteres[-1]
        for compagnie in compagnies:
            routes_0, routes_1, routes_2 = compagnie.chercher_routes(aer_dep, aer_arr, escales_max)
            routes_directes.extend(routes_0)
            routes_1escale.extend(routes_1)
            routes_2escales.extend(routes_2)

        print("routes directes")
        for route in routes_directes:
            print(route)
        print("routes 1 escale")
        for routes in routes_1escale:
            print(*routes)
        print("routes 2 escales")
        for routes in routes_2escales:
            print(*routes)
        return

    @staticmethod
    def saisie_criteres(aeroports):
        """
        Methode qui permet de saisir les criteres pour choisir un vol
        
        :param aeroports: listes des aeroports
        :return: un tuple avec les différentes informations : aeroport de depart, aeroport d'arrivee, date de depart
        date de retour, nombre d'adulte, nombre d'enfant, classe, nombre max d'escales
        """

        # Demander l'aéroport départ et l'aéroport arrivée
        aer_dep     = saisie_aeroport("aéroport de départ", aeroports)
        aer_arr     = saisie_aeroport("aéroport d'arrivée", aeroports)
        # Demander les dates départ et retour
        date_dep    = saisie_date("date de départ", datetime.today())
        date_arr    = saisie_date("date de retour", date_dep)
        # Demander le nombre de passagers (adultes/enfants)
        nb_adultes  = Client.saisie_passagers("adultes (12 ans et +)")
        nb_enfants  = Client.saisie_passagers("enfants (- de 12 ans)")
        # Demander quelle classe
        classe      = Client.saisie_classe()
        # Demander le nombre d'escales
        escales_max = Client.saisie_nb_escales()
        return [aer_dep, aer_arr, date_dep, date_arr,
                nb_adultes, nb_enfants, classe, escales_max]

    @staticmethod
    def saisie_passagers(message):
        """
        Methode qui permet de saisir les informations concernant un passager 
        
        :param message: message que l'on veut transmettre au passager
        :return: le nombre de passager
        """

        liste_choix = ["0 passager",]
        liste_choix.extend(["{} passagers".format(x) for x in range(1,6)])
        nb_passagers = ihm.choisir(
            liste_choix, "Saisissez le nombre de voyageurs {} :".format(message))
        ihm.afficher("Vous avez choisi {} {}".format(nb_passagers, message))
        nb_passagers = int(nb_passagers[0])
        return nb_passagers

    @staticmethod
    def saisie_classe():
        """
        Methode qui permet de choisir la classe de la place
        :return: la classe choisie
        """

        liste_choix = {
            "Première" : 'F',
            "Business" : 'C',
            "Premium Eco" : 'P',
            "Economique" : 'Y'
        }
        classe = ihm.choisir([*liste_choix.keys()], "Choisissez une classe :")
        ihm.afficher("Vous avez choisi {}".format(classe))
        return liste_choix[classe]

    @staticmethod
    def saisie_nb_escales():
        """
        Methode pour choisir combien d'escale le passager souhaite avoir au maximum
        
        :return: le type de vol qu'il a choisi entre aucune, une ou deux escales
        """

        liste_choix = ["Vol direct seulement","Jusqu'à 1 escale","Jusqu'à 2 escales"]
        type_vol = ihm.choisir(liste_choix, "Choisissez un type de vol :")
        ihm.afficher("Vous avez choisi : {}".format(type_vol))
        return liste_choix.index(type_vol)

    def consulter_reservations(self):
        """
        Methode qui permet d'afficher la liste de toutes les reservations effectuees
        :return: None
        """

        resas_tri = self._reservations
        resas_tri.sort(key=lambda s: s.date_achat, reverse=True)
        ihm.afficher("Il y a {} réservation(s)".format(len(resas_tri)))
        ihm.afficher_paginer(resas_tri, "Réservations", pas=10)
        return

    def annuler_reservation(self, resa):
        """
        Methode qui permet de supprimer la reservation
        :return: 
        """
        pass

