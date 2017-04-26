class TypeAvion(object):
    def __init__(self, id_type_avion, nb_place_premiere, nb_place_business, nb_place_eco_plus, nb_place_economique, nb_total_place, fuel_cap_L, distance_franchissable_km, coefficient_cout, vitesse_mach, altitude_vol_m, distance_decollage_m):
        """
        Constructeur de la classe typeAvion
        
        :param id_type_avion: identifiant du type de l'avion
        :param nb_place_premiere: nombre de place de premiere dans l'avion
        :param nb_place_business: nombre de place de business dans l'avion
        :param nb_place_eco_plus: nombre de place eco plus dans l'avion
        :param nb_place_economique: nombre de place economique dans l'acion
        :param nb_total_place: nombre total de place dans l'avion
        :param fuel_cap_L: capacité total en fuel de l'avion en L
        :param distance_franchissable_km: distance maximale que l'avion peut faire sans atterir
        :param coefficient_cout: le coefficient de cout de l'avion 
        :param vitesse_mach: vitesse de l'avion en mach
        :param altitude_vol_m: l'altitude de croisière de l'avion
        :param distance_decollage_m: la distance necessaire a l'avion pour decoller
        """

        self._id_type_avion = id_type_avion
        self._nb_place_premiere  = nb_place_premiere
        self._nb_place_business  = nb_place_business
        self._nb_place_eco_plus  = nb_place_eco_plus
        self._nb_place_economique  = nb_place_economique
        self._nb_total_place  = nb_total_place
        self._fuel_cap_L  = fuel_cap_L
        self._distance_franchissable_km  = distance_franchissable_km
        self._coefficient_cout  = coefficient_cout
        self._vitesse_mach  = vitesse_mach
        self._altitude_vol_m  = altitude_vol_m
        self._distance_decollage_m  = distance_decollage_m

    @property
    def id_type_avion(self):
        return self._id_type_avion

    @property
    def nb_place_premiere(self):
        return self._nb_place_premiere

    @property
    def nb_place_business(self):
        return self._nb_place_business

    @property
    def nb_place_eco_plus(self):
        return self._nb_place_eco_plus

    @property
    def nb_place_economique(self):
        return self._nb_place_economique

    @property
    def nb_total_place(self):
        return self._nb_total_place

    @property
    def fuel_cap_L(self):
        return self._fuel_cap_L

    @property
    def distance_franchissable_km(self):
        return self._distance_franchissable_km

    @property
    def coefficient_cout(self):
        return self._coefficient_cout

    @property
    def vitesse_mach(self):
        return self._vitesse_mach

    @property
    def altitude_vol_m(self):
        return self._altitude_vol_m

    @property
    def distance_decollage_m(self):
        return self._distance_decollage_m

