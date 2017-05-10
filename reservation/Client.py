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
        criteres = self.saisie_criteres(aeroports)
        aer_dep, aer_arr, date_dep, date_arr, \
            nb_passagers, classe, escales_max = criteres

        # Recherche des routes
        combinaisons_total = []
        for compagnie in compagnies:
            combinaisons = compagnie.chercher_routes_escales(
                aer_dep, aer_arr, escales_max)
            if combinaisons:
                combinaisons_total.extend(combinaisons)

        # Affiche les prix, distances
        self.affiche_prix_distance(combinaisons_total, classe)

        # On garde seulement les combinaisons avec horaires en base
        combinaisons_avec_horaires = []
        for combi in combinaisons_total:
            combi_ok = True
            for route in combi:
                if len(route.horaires) == 0:
                    combi_ok = False
            if combi_ok:
                combinaisons_avec_horaires.append(combi)

        # On recupere les vols pour chaque combinaison
        combi_vols = self.recupere_vols(
            combinaisons_avec_horaires, date_dep, nb_passagers, classe)

        # On filtre les vols pour qu'ils s'enchainent bien
        vols_ok = self.arrange_vols(combi_vols, date_dep)

        ihm.afficher("Parmi les routes, {} possédaient des places a la date demandée"
                     .format(len(vols_ok)))
        combi_test = []
        for combi in vols_ok:
            combi_new = []
            for route, vols in combi:
                combi_new.append(route)
            combi_test.append(combi_new)
        choix_combi = self.affiche_prix_distance(combi_test, classe, choix=True)

        combi = vols_ok[choix_combi]
        for route, vols in combi:
            ihm.afficher("Vols disponibles pour la route {} :".format(route))
            vol = ihm.choisir_paginer(vols, "Choisissez un vol :")
            ihm.afficher("Choisissez une place pour ce vol (les places libres sont représentées par un O) :")
            vol.afficher_places()
            place = ihm.demander("Saisissez le numéro de la place (ex : 35A) :")
            vol.reserver_place(place[:-1],place[-1])
            print(place)
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
        date_ret = None
        aller_retour = ihm.choisir(['Oui','Non'], "Voulez-vous un retour ?")
        if aller_retour == 'Oui':
            date_ret    = saisie_date("date de retour", date_dep)
        # Demander le nombre de passagers
        nb_passagers  = Client.saisie_passagers()
        # Demander quelle classe
        classe      = Client.saisie_classe()
        # Demander le nombre d'escales
        escales_max = Client.saisie_nb_escales()

        return [aer_dep, aer_arr, date_dep, date_ret,
                nb_passagers, classe, escales_max]

    @staticmethod
    def saisie_passagers():
        """
        Methode qui permet de saisir les informations concernant un passager 
        
        :return: le nombre de passager
        """

        liste_choix = ["0 passager",]
        liste_choix.extend(["{} passagers".format(x) for x in range(1,6)])
        nb_passagers = ihm.choisir(
            liste_choix, "Saisissez le nombre de voyageurs :")
        ihm.afficher("Vous avez choisi {} passagers".format(nb_passagers))
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

    @staticmethod
    def affiche_prix_distance(combinaisons, classe, choix=False):
        combi_prix = []
        combi_dist = []
        combi_tout = []
        for combi in combinaisons:
            prix_combi = 0
            dist_totale = 0
            for route in combi:
                prix_combi += route.calcul_prix_route(classe)
                dist_totale += route.distance/1000
            combi_prix.append(prix_combi)
            combi_dist.append(dist_totale)
        combi_tout.extend(zip(combinaisons, combi_prix, combi_dist))

        combi_print = []
        combi_tout.sort(key=lambda s: s[1])
        for combi in combi_tout:
            ligne = "{:.2f}€".format(combi[1])
            ligne += " {:.0f}km".format(combi[2])
            route0 = combi[0][0]
            ligne += " - {} - {} ({},{})".format(
                route0.compagnie.code_icao,
                route0.aeroport_depart.id_code_iata,
                route0.aeroport_depart.municipalite,
                route0.aeroport_depart.code_pays)
            for route in combi[0]:
                ligne += " -> {} ({},{})".format(
                    route.aeroport_arrivee.id_code_iata,
                    route.aeroport_arrivee.municipalite,
                    route.aeroport_arrivee.code_pays)
            combi_print.append(ligne)

        if choix:
            trajet = ihm.choisir_paginer(combi_print, "Choisissez un trajet")
            return combi_print.index(trajet)
        else:
            ihm.afficher_paginer(combi_print, "Liste des trajets trouvés")
        return

    @staticmethod
    def recupere_vols(combinaisons, jour_depart, nb_passagers, classe):
        """
        Recupere les vols avec places d'une date donnnee (et jour suivant)
        
        :param combinaisons: 
        :param jour_depart: 
        :param nb_passagers:
        :param classe: 
        :return: 
        """
        combi_vols = []
        for combi in combinaisons:
            routes_vols = []
            combi_ok = True
            # Pour chaque route de la combinaison
            for route in combi:
                vols_tout = route.chercher_vols(jour_depart, nb_passagers, classe)
                # Si on a trouve des vols pour la route, on enregistre
                if vols_tout:
                    routes_vols.append([route, vols_tout])
                # Sinon la route n'est pas disponible
                else:
                    combi_ok = False
                    break
            if combi_ok:
                combi_vols.append(routes_vols)

        return combi_vols

    @staticmethod
    def arrange_vols(combi_vols, jour_depart):
        """
        Filtre les vols d'une suite de route pour qu'ils puissent s'enchainer
        
        :param combi_vols: 
        :param jour_depart: 
        :return: 
        """

        jour_depart = jour_depart.date()
        vols_ok = []
        for combi in combi_vols:
            route, vols = combi[0]
            # Si le trajet n'a pas d'escale, on enregistre tous les vols du jour
            if len(combi) == 1:
                vols = [x for x in vols if x.datetime_depart.date() == jour_depart]
                vols_ok.append([[route, vols]])
            # Sinon
            else:
                # On regarde la premiere arrivee + 20 minutes
                premiere_arrivee = vols[0].datetime_arrivee
                premiere_arrivee += timedelta(minutes=20)
                route2, vols2 = combi[1]
                # Parmi les vols en correspondance, on enleve ceux avant la premiere arrivee
                # On prend les vols du jour demande de preference
                vols2_jour = [x for x in vols2 if x.datetime_depart > premiere_arrivee
                              and x.datetime_depart.date() == jour_depart]
                # Sinon on prend le jour d'apres
                if len(vols2_jour) == 0:
                    vols2_jour = [x for x in vols2
                                  if x.datetime_depart > premiere_arrivee]
                vols2 = vols2_jour
                # On regarde le dernier depart de correspondance - 20 minutes
                dernier_depart = vols2[-1].datetime_depart
                dernier_depart -= timedelta(minutes=20)
                # On enleve les vols qui arrivent apres le dernier depart
                vols = [x for x in vols if x.datetime_arrivee < dernier_depart]
                # Si le trajet ne comporte qu'une seule escale, on enregistre
                if len(combi) == 2:
                    vols_ok.append([[route, vols], [route2, vols2]])
                # Sinon
                else:
                    # Meme chose
                    premiere_arrivee = vols2[0].datetime_arrivee
                    premiere_arrivee += timedelta(minutes=20)
                    route3, vols3 = combi[2]
                    # On garde ceux qui partent apres la premiere arrivee
                    vols3_jour = [x for x in vols3 if x.datetime_depart > premiere_arrivee
                                  and x.datetime_depart.date() == jour_depart]
                    if len(vols3_jour) == 0:
                        vols3_jour = [x for x in vols3
                                      if x.datetime_depart > premiere_arrivee]
                    vols3 = vols3_jour
                    # On garde ceux qui arrivent avant le dernier depart
                    dernier_depart = vols3[-1].datetime_depart
                    dernier_depart -= timedelta(minutes=20)
                    vols2 = [x for x in vols2 if x.datetime_arrivee < dernier_depart]
                    dernier_depart = vols2[-1].datetime_depart
                    dernier_depart -= timedelta(minutes=20)
                    vols = [x for x in vols if x.datetime_arrivee < dernier_depart]
                    # On enregistre
                    vols_ok.append([[route, vols], [route2, vols2_jour], [route3, vols3]])

        return vols_ok

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
