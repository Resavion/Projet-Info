class Aeroport(object):
    def __init__(self, id_aero, type, nom, latitude, longtitude, elevation, code_continent,
                 code_pays, municipalite, gps_code):
        """
        Constructeur de la classe aeroport
        
        :param id_aero: identifiant de l'aeroport correspondant au iata code
        :param type: type de l'aeroport (grand, moyen, petit)
        :param nom: nom de l'aeroport
        :param latitude: la latitude de l'aeroport
        :param longtitude: la longitude de l'aeroport
        :param elevation: l'elevation de l'aeroport
        :param code_continent: le code du continent ou se trouve l'aeroport
        :param code_pays: le code du pays ou se trouve l'aeroport
        :param municipalite: la municipalite ou se trouve l'aeroport
        :param gps_code: le code gps de l'aeroport
        """
        self._id_aero = id_aero
        self._type = type
        self._nom = nom
        self._latitude = latitude
        self._longtitude = longtitude
        self._elevation = elevation
        self._code_continent = code_continent
        self._code_pays = code_pays
        self._municipalite = municipalite
        self._gps_code = gps_code

    @property
    def id_aero(self):
        return

    @property
    def type(self):
        return self._type

    @property
    def nom(self):
        return self._nom

    @property
    def latitude(self):
        return self._latitude

    @property
    def longtitude(self):
        return self._longtitude

    @property
    def elevation(self):
        return self._elevation

    @property
    def code_continent(self):
        return self._code_continent


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
