class Aeroport(object):
    def __init__(self, id_code_iata, type_aero, nom, latitude_deg, longitude_deg,
                 elevation_ft, code_continent, code_pays, municipalite, code_icao,
                 pistes=None, avions=None, routes_entrantes=None, routes_sortantes=None):
        """
        Constructeur de la classe aeroport
        
        :param id_code_iata: identifiant de l'aeroport correspondant au iata code
        :param type_aero: type de l'aeroport (grand, moyen, petit)
        :param nom: nom de l'aeroport
        :param latitude_deg: la latitude de l'aeroport
        :param longitude_deg: la longitude de l'aeroport
        :param elevation_ft: l'elevation de l'aeroport
        :param code_continent: le code du continent ou se trouve l'aeroport
        :param code_pays: le code du pays ou se trouve l'aeroport
        :param municipalite: la municipalite ou se trouve l'aeroport
        :param code_icao: le code gps de l'aeroport
        :param pistes: liste des pistes de l'aeroport
        :param avions: avions presents sur l'aeroport
        :param routes_entrantes: routes arrivant a l'aeroport
        :param routes_sortantes: routes parant de l'aeroport
        """
        self._id_code_iata = id_code_iata
        self._type_aero = type_aero
        self._nom = nom
        self._latitude_deg = latitude_deg
        self._longitude_deg = longitude_deg
        self._elevation_ft = elevation_ft
        self._code_continent = code_continent
        self._code_pays = code_pays
        self._municipalite = municipalite
        self._code_icao = code_icao
        if pistes is None:
            pistes = []
        self._pistes = pistes
        if avions is None:
            avions = []
        self._avions = avions
        if routes_entrantes is None:
            routes_entrantes = []
        self._routes_entrantes = routes_entrantes
        if routes_sortantes is None:
            routes_sortantes = []
        self._routes_sortantes = routes_sortantes

    @property
    def id_code_iata(self):
        return self._id_code_iata

    @property
    def type_aero(self):
        return self._type_aero

    @property
    def nom(self):
        return self._nom

    @property
    def latitude_deg(self):
        return self._latitude_deg

    @property
    def longitude_deg(self):
        return self._longitude_deg

    @property
    def elevation_ft(self):
        return self._elevation_ft

    @property
    def code_continent(self):
        return self._code_continent

    @property
    def code_pays(self):
        return self._code_pays

    @property
    def municipalite(self):
        return self._municipalite

    @property
    def code_icao(self):
        return self._code_icao

    @property
    def pistes(self):
        return self._pistes

    @property
    def avions(self):
        return self._avions

    @property
    def routes_entrantes(self):
        return self._routes_entrantes

    @property
    def routes_sortantes(self):
        return self._routes_sortantes

    def __str__(self):
        return "{} {}, {}, {} (IATA : {}, ICAO : {})"\
            .format(self._id_code_iata, self._nom,
                    self._municipalite, self._code_pays,
                    self._id_code_iata, self._code_icao)

    def afficher_routes(self):
        """
        Methode qui permet d'afficher toutes les routes possibles qui partent d'un aeroport donné
        :return: 
        """
        pass

    def afficher_horaires(self):
        """
        Methode qui permet d'afficher tous les vols d'arrivée et de départ de l'aéroport
         
        :return: 
        """
        pass

    def afficher_vols(self):
        """
        Methode qui permet d'afficher tous les vols d'arrivee et de depart de l'aéroport un jour donné
        :return: 
        """
        pass
