class Aeroport(object):
    def __init__(self, id_aero, type_aero, nom, latitude_deg, longtitude_deg, elevation_ft, code_continent,
                 code_pays, municipalite, gps_code, pistes):
        """
        Constructeur de la classe aeroport
        
        :param id_aero: identifiant de l'aeroport correspondant au iata code
        :param type_aero: type de l'aeroport (grand, moyen, petit)
        :param nom: nom de l'aeroport
        :param latitude_deg: la latitude de l'aeroport
        :param longtitude_deg: la longitude de l'aeroport
        :param elevation_ft: l'elevation de l'aeroport
        :param code_continent: le code du continent ou se trouve l'aeroport
        :param code_pays: le code du pays ou se trouve l'aeroport
        :param municipalite: la municipalite ou se trouve l'aeroport
        :param gps_code: le code gps de l'aeroport
        :param pistes: liste des pistes de l'aeroport
        """
        self._id_aero = id_aero
        self._type_aero = type_aero
        self._nom = nom
        self._latitude_deg = latitude_deg
        self._longtitude_deg = longtitude_deg
        self._elevation_ft = elevation_ft
        self._code_continent = code_continent
        self._code_pays = code_pays
        self._municipalite = municipalite
        self._gps_code = gps_code
        self._pistes = pistes

    @property
    def id_aero(self):
        return self._id_aero

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
    def longtitude_deg(self):
        return self._longtitude_deg

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
    def gps_code(self):
        return self._gps_code


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
