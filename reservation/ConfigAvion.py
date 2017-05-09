class ConfigAvion(object):
    def __init__(self, compagnie, nom, type_avion, nb_places_premiere, nb_places_business,
                 nb_places_eco_plus, nb_places_eco, nb_total_places, disposition):
        """
        Constructeur de la classe ConfigAvion
        
        :param compagnie: compagnie qui utilise cette configuration
        :param nom: nom de la configuration d'avion
        :param type_avion: type de l'avion
        :param nb_places_premiere: nombre de place de premiere dans l'avion
        :param nb_places_business: nombre de place de business dans l'avion
        :param nb_places_eco_plus: nombre de place eco plus dans l'avion
        :param nb_places_eco: nombre de place economique dans l'avion
        :param nb_total_places: nombre total de place dans l'avion
        :param disposition: schema des places dans l'avion
        """
        self._compagnie          = compagnie
        self._nom                = nom
        self._type_avion = type_avion
        self._nb_places_premiere = nb_places_premiere
        self._nb_places_business = nb_places_business
        self._nb_places_eco_plus = nb_places_eco_plus
        self._nb_places_eco      = nb_places_eco
        self._nb_total_places    = nb_total_places
        self._disposition        = disposition

    @property
    def nom(self):
        return self._nom

    @property
    def compagnie(self):
        return self._compagnie

    @property
    def type_avion(self):
        return self._type_avion

    @property
    def nb_places_premiere(self):
        return self._nb_places_premiere

    @property
    def nb_places_business(self):
        return self._nb_places_business

    @property
    def nb_places_eco_plus(self):
        return self._nb_places_eco_plus

    @property
    def nb_places_eco(self):
        return self._nb_places_eco

    @property
    def nb_total_places(self):
        return self._nb_total_places

    @property
    def disposition(self):
        return self._disposition

    def __str__(self):
        return "{} {} ({}) : {}F/{}C/{}P/{}Y : {} pax"\
            .format(self._compagnie.id_code_iata, self._nom,
                    self._type_avion, self._nb_places_premiere,
                    self._nb_places_business, self._nb_places_eco_plus,
                    self._nb_places_eco, self._nb_total_places)