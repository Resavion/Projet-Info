from datetime import (datetime, timedelta)

import ihm.console as ihm


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
        self._id = id_client
        self._nom = nom
        self._prenom = prenom
        self._date_naissance = date_naissance
        if reservations is None:
            reservations = []
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
        :return: 
        """
        self.saisir_criteres(aeroports)
        return

    @staticmethod
    def saisir_criteres(aeroports):
        # Demander l'aéroport départ et l'aéroport arrivée
        aer_dep = Client.saisie_aeroport("aéroport de départ", aeroports)
        aer_arr = Client.saisie_aeroport("aéroport d'arrivée", aeroports)
        # Demander les dates départ et retour
        date_dep = Client.saisie_date("date de départ", datetime.today())
        date_arr = Client.saisie_date("date d'arrivée", date_dep)
        print(date_dep, date_arr)
        # Demander le nombre de passagers (adultes/enfants)
        # Demander quelle classe
        return

    @staticmethod
    def saisie_aeroport(message, aeroports):
        aero = None
        while aero is None:
            code = ihm.demander(
                "Saisissez l'{} (code IATA ou ICAO ou ville) :".format(message))
            results = [x for x in aeroports
                       if x.id_code_iata == code or x.code_icao == code or
                       x.municipalite.startswith(code)]
            if len(results) == 0:
                ihm.afficher("Désolé, nous n'avons pas trouvé votre aéroport !")
            elif len(results) > 1:
                aero = ihm.choisir_paginer(results, "Précisez votre choix :")
            else:
                aero = results[0]
        ihm.afficher("Vous avez choisi : {}".format(aero))
        return aero

    @staticmethod
    def saisie_date(message, date_seuil):
        date_saisie = None
        dans1an = date_seuil.replace(year=date_seuil.year + 1)
        while True:
            try:
                date_saisie = ihm.demander(
                    "Saisissez votre {} (AAAA-MM-JJ) :".format(message))
                date_saisie = datetime.strptime(date_saisie, '%Y-%m-%d')
                if date_saisie <= date_seuil or date_saisie > dans1an:
                    raise ValueError
            except ValueError:
                ihm.afficher("Ceci n'est pas une date valide.")
                pass
            else:
                break
        return date_saisie

    def consulter_reservations(self):
        ihm.afficher("Il y a {} réservation(s)".format(len(self._reservations)))
        ihm.afficher_paginer(self._reservations, "Réservations", pas=10)
        return

    def consulter_reservation(self):
        """
        Methode qui permet d'afficher la reservation au client avec les différentes informations pour le vol
        :return: 
        """
        pass

    def modifier_reservation(self):
        """
        Methode qui permet de modifier la reservation (date, vol etc)
        :return: 
        """
        pass

    def annuler_reservation(self):
        """
        Methode qui permet de supprimer la reservation
        :return: 
        """
        pass

