class Compagnie(object):
    def __init__(self, id_code_iata, nom, code_icao, pays, code_continent, code_pays,
                 configs=None, avions=None, routes=None):
        """
         Constructeur de la classe compagnie
        
        :param id_code_iata: identifiant de la compagnie qui correspond au code iata
        :param nom: nom de la compagnie
        :param code_icao: code icao de la compagnie
        :param pays: pays d'origine de la compagnie
        :param code_continent: code du continent
        :param code_pays: code du pays
        :param configs: liste des configs d'avions proposees par la compagnie
        :param avions: liste des avions possedes par la compagnie
        :param routes: liste des routes assurees par la compagnie
        """
        self._id_code_iata = id_code_iata
        self._nom = nom
        self._code_icao = code_icao
        self._pays = pays
        self._code_continent = code_continent
        self._code_pays = code_pays
        if configs is None:
            configs = []
        self._configs = configs
        if avions is None:
            avions = []
        self._avions = avions
        if routes is None:
            routes = []
        self._routes = routes

    @property
    def id_code_iata(self):
        return self._id_code_iata

    @property
    def nom(self):
        return self._nom

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
    def code_pays(self):
        return self._code_pays

    @property
    def configs(self):
        return self._configs

    @property
    def avions(self):
        return self._avions

    @property
    def routes(self):
        return self._routes

    def __str__(self):
        return "{}, {} (IATA : {}, ICAO : {})"\
            .format(self._nom, self._pays,
                    self._id_code_iata, self._code_icao)

    def afficher_routes(self):
        """
        Methode qui permet d'afficher les routes proposees par la compagnie
        :return: 
        """
        for route in self._routes:
            print(route)
        return

    def ajouter_route(self):
        """
        Methode qui permet d'ajouter une route empruntée par la compagnie pour un vol
        :return: 
        """
        pass

    def suspendre_route(self):
        """
        Methode pour suspendre une route proposee par la compagnie
        :return: 
        """
        pass

    def afficher_avions(self):
        """
        Methode qui permet d'afficher l'emplacement des différents avions
        :return: 
        """
        for avion in self._avions:
            print(avion)
        return

    def affecter_avion(self):
        """
        Methode qui permet d'affecter un avion existant à un vol

        :return: 
        """
        pass

    def afficher_stats(self):
        """
        Methode qui permet d'afficher les statistiques sur le nombre de passager, etc pour la compagnie
        :return: 
        """
        pass



    