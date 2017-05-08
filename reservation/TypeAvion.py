class TypeAvion(object):
    def __init__(self, id, nom, code_iata, code_icao, fuel_cap_L, distance_franchissable_km,
                 vitesse_mach, altitude_vol_m, distance_decollage_m):
        """
        Constructeur de la classe typeAvion
        
        :param id: identifiant du type de l'avion
        :param nom: nom complet du type de l'avion
        :param code_iata: code IATA du type de l'avion
        :param code_icao: code ICAO du type de l'avion
        :param fuel_cap_L: capacité total en fuel de l'avion en L
        :param distance_franchissable_km: distance maximale que l'avion peut faire sans atterir
        :param vitesse_mach: vitesse de l'avion en mach
        :param altitude_vol_m: l'altitude de croisière de l'avion
        :param distance_decollage_m: la distance necessaire a l'avion pour decoller
        """
        self._id = id
        self._nom = nom
        self._code_iata = code_iata
        self._code_icao = code_icao
        self._fuel_cap_L = fuel_cap_L
        self._distance_franchissable_km = distance_franchissable_km
        self._vitesse_mach = vitesse_mach
        self._altitude_vol_m = altitude_vol_m
        self._distance_decollage_m = distance_decollage_m

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def code_iata(self):
        return self._code_iata

    @property
    def code_icao(self):
        return self._code_icao

    @property
    def fuel_cap_L(self):
        return self._fuel_cap_L

    @property
    def distance_franchissable_km(self):
        return self._distance_franchissable_km

    @property
    def coefficient_cout(self):
        pass

    @property
    def vitesse_mach(self):
        return self._vitesse_mach

    @property
    def altitude_vol_m(self):
        return self._altitude_vol_m

    @property
    def distance_decollage_m(self):
        return self._distance_decollage_m

    def __str__(self):
        return "{}".format(self._nom)
