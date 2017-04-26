class Compagnie(object):
    def __init__(self, id_compagnie, nom_compagnie, alias, iata, icao, callsign, pays, actif):
        """
        Constructeur de la classe compagnie
        
        :param id_compagnie: identifiant de la compagnie
        :param nom_compagnie: nom de la compagnie
        :param alias: alias de la compagnie
        :param iata: code iata de la compagnie
        :param icao: code icao de la compagnie
        :param callsign: callsigne de la compagnie
        :param pays: pays d'origine de la compagnie
        :param actif: si la compagnie est toujours active
        """

        self._id_compagnie = id_compagnie
        self._nom_compagnie = nom_compagnie
        self._alias = alias
        self._iata = iata
        self._icao = icao
        self._callsign = callsign
        self._pays = pays
        self._actif= actif

    @property
    def id_compagnie(self):
        return self._id_compagnie

    @property
    def nom_compagnie(self):
        return self._nom_compagnie

    @property
    def alias(self):
        return self._alias

    @property
    def iata(self):
        return self._iata

    @property
    def icao(self):
        return self._icao

    @property
    def callsign(self):
        return self._callsign

    @property
    def pays(self):
        return self._pays

    @property
    def actif(self):
        return self._actif



def ajouter_route(self):
"""
        Methode qui permet d'ajouter une route empruntée par la compagnie pour un vol
        :return: 
        """
        pass

    def supprimer_route(self):
        """
        Methode pour supprimer une route au préalablement assignée à un vol
        :return: 
        """
        pass


    def afficher_stats(self):
        """
        Methode qui permet d'afficher les statistiques sur le nombre de passager, etc pour la compagnie
        :return: 
        """
        pass

    def afficher_avions(self):
        """
        Methode qui permet d'afficher l'emplacement des différents avions
        :return: 
        """
        pass


    def afficher_routes(self):
        """
        Methode qui permet d'afficher le chemin suivi par le passager avec les escales
        :return: 
        """
        pass

    def affecter_avion(self):
        """
        Methode qui permet d'affecter un avion existant à un vol
        
        :return: 
        """
        pass



    