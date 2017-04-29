class ConfigAvion(object):
    def __init__(self, id_config_avion, nom, compagnie, type_avion, nb_place_premiere, nb_place_business,
                 nb_place_eco_plus, nb_place_eco, nb_total_place, disposition):
        """
        Constructeur de la classe ConfigAvion
        
        :param id_config_avion: identifiant de la configuration d'avion
        :param nom: nom de la configuration d'avion
        :param compagnie: compagnie qui utilise cette configuration
        :param type_avion: type de l'avion
        :param nb_place_premiere: nombre de place de premiere dans l'avion
        :param nb_place_business: nombre de place de business dans l'avion
        :param nb_place_eco_plus: nombre de place eco plus dans l'avion
        :param nb_place_eco: nombre de place economique dans l'avion
        :param nb_total_place: nombre total de place dans l'avion
        :param disposition: schema des places dans l'avion
        """
        self._id_config_avion = id_config_avion
        self._nom = nom
        self._compagnie = compagnie
        self._type_avion = type_avion
        self._nb_place_premiere = nb_place_premiere
        self._nb_place_business = nb_place_business
        self._nb_place_eco_plus = nb_place_eco_plus
        self._nb_place_eco = nb_place_eco
        self._nb_total_place = nb_total_place
        self._disposition = disposition

    @property
    def id_config_avion(self):
        return self._id_config_avion

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
    def nb_place_premiere(self):
        return self._nb_place_premiere

    @property
    def nb_place_business(self):
        return self._nb_place_business

    @property
    def nb_place_eco_plus(self):
        return self._nb_place_eco_plus

    @property
    def nb_place_eco(self):
        return self._nb_place_eco

    @property
    def nb_total_place(self):
        return self._nb_total_place

    @property
    def disposition(self):
        return self._disposition

    def __str__(self):
        return "{} {} ({}) : {}F,{}C,{}P,{}Y : {} pax"\
            .format(self._compagnie.id_compagnie,self._nom,
                    self._type_avion,self._nb_place_premiere,
                    self._nb_place_business,self._nb_place_eco_plus,
                    self._nb_place_eco,self._nb_total_place)