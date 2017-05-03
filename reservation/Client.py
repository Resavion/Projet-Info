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
        criteres = self.saisir_criteres(aeroports)
        self.afficher_vols(criteres, compagnies, aeroports)
        return

    @staticmethod
    def saisir_criteres(aeroports):
        # Demander l'aéroport départ et l'aéroport arrivée
        aer_dep = Client.saisie_aeroport("aéroport de départ", aeroports)
        aer_arr = Client.saisie_aeroport("aéroport d'arrivée", aeroports)
        # Demander les dates départ et retour
        date_dep = Client.saisie_date("date de départ", datetime.today())
        date_arr = Client.saisie_date("date de retour", date_dep)
        # Demander le nombre de passagers (adultes/enfants)
        nb_adultes = Client.saisie_passagers("adultes (12 ans et +)")
        nb_enfants = Client.saisie_passagers("enfants (- de 12 ans)")
        # Demander quelle classe
        classe = Client.saisie_classe()
        # Demander le nombre d'escales
        escales_max = Client.saisie_nb_escales()
        return [aer_dep, aer_arr, date_dep, date_arr,
                nb_adultes, nb_enfants, classe, escales_max]

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
        ihm.afficher("Vous avez choisi le {:%d/%m/%Y}".format(date_saisie))
        return date_saisie

    @staticmethod
    def saisie_passagers(message):
        liste_choix = ["0 passager",]
        liste_choix.extend(["{} passagers".format(x) for x in range(1,6)])
        nb_passagers = ihm.choisir(
            liste_choix, "Saisissez le nombre de voyageurs {} :".format(message))
        ihm.afficher("Vous avez choisi {} {}".format(nb_passagers, message))
        nb_passagers = int(nb_passagers[0])
        return nb_passagers

    @staticmethod
    def saisie_classe():
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
        liste_choix = ["Vol direct seulement","Jusqu'à 1 escale","Jusqu'à 2 escales"]
        type_vol = ihm.choisir(liste_choix, "Choisissez un type de vol :")
        ihm.afficher("Vous avez choisi : {}".format(type_vol))
        return liste_choix.index(type_vol)

    @staticmethod
    def chercher_vols(criteres, compagnies):
        aer_dep, aer_arr, date_dep, date_arr = criteres[:4]
        nb_adultes, nb_enfants, classe, escales_max = criteres[4:]

        routes_directes = []
        routes_1escale = []
        routes_2escales = []

        for compagnie in compagnies:
            routes = [x for x in compagnie.routes if x.aeroport_depart == aer_dep]
            aeroports_visites = [aer_dep]
            route_directe = [x for x in routes if x.aeroport_arrivee == aer_arr]
            if route_directe:
                routes_directes.extend(route_directe)

            if escales_max > 0:
                routes_indirectes = [x for x in routes if x.aeroport_arrivee != aer_arr]
                aeroports_visites.extend([x.aeroport_arrivee for x in routes_indirectes])

                for route_indirecte in routes_indirectes:
                    routes_sortantes, route_1escale = Client.routes_avec_1escale(
                        compagnie, aeroports_visites, route_indirecte, aer_arr
                    )
                    if route_1escale:
                        routes_1escale.append(route_1escale)

                    if escales_max > 1:
                        for route_sortante in routes_sortantes:
                            route_2escales = Client.route_avec_2escales(
                                compagnie, route_indirecte, route_sortante, aer_arr
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
            return routes2, [route1, route_1escale]
        return routes2

    @staticmethod
    def route_avec_2escales(compagnie, route1, route2, aer_arr):
        escale = route2.aeroport_arrivee
        route_2escales = [
            x for x in compagnie.routes
            if x.aeroport_depart == escale and x.aeroport_arrivee == aer_arr
        ]
        if route_2escales:
            return [route1, route2, route_2escales]
        return None


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

