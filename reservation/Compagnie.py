class Compagnie(object):
    def __init__(self, id_compagnie, nom_compagnie, code_icao, pays, code_continent, code_pays):
        """
         Constructeur de la classe compagnie
        
        :param id_compagnie: identifiant de la compagnie
        :param nom_compagnie: nom de la compagnie
        :param code_icao: code icao de la compagnie
        :param pays: pays d'origine de la compagnie
        :param code_continent: code du continent
        :param code_pays: code du pays
        """


        self._id_compagnie = id_compagnie
        self._nom_compagnie = nom_compagnie
        self._code_icao = code_icao
        self._pays = pays
        self._code_continent = code_continent
        self._code_pays = code_pays

    @property
    def id_compagnie(self):
        return self._id_compagnie

    @property
    def nom_compagnie(self):
        return self._nom_compagnie

    @property
    def code_icao(self):
        return self._code_icao

    @property
    def pays(self):
        return self._pays

    @property
    def code_continent(self):
        return self._code_continent

    @property
    def code_paysself):
        return self._code_pays


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



    