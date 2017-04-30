from datetime import date


class Avion(object):
    def __init__(self, id_avion, compagnie, config, aeroport, date_construction, date_derniere_revision,
                 etat, position):
        """
        Constructeur de la classe avion
        
        :param id_avion: identifiant avion
        :param compagnie: compagnie qui possède l'avion
        :param config: configuration de l'avion
        :param aeroport: aeroport ou il se situe actuellement
        :param date_construction: date de construction de l'avion
        :param date_derniere_revision: derniere date de revision de l'avion
        :param etat: donne l'etat de l'avion, si il est en vol, au sol, non utilisable
        :param position: la position de l'avion en fonction de ses coordonnées
        """
        self._id = id_avion
        self._compagnie = compagnie
        self._config = config
        self._date_construction = date_construction
        self._date_derniere_revision = date_derniere_revision
        self._etat = etat
        self._aeroport = aeroport
        self._position = position

    @property
    def id(self):
        return self._id

    @property
    def compagnie(self):
        return self._compagnie

    @property
    def config(self):
        return self._config

    @property
    def date_construction(self):
        return self._date_construction

    @property
    def date_derniere_revision(self):
        return self._date_derniere_revision

    @property
    def etat(self):
        return self._etat

    @property
    def aeroport(self):
        return self._aeroport

    @property
    def position(self):
        return self._position

    @property
    def age(self):
        when = self._date_construction
        on = date.today()
        was_earlier = (on.month, on.day) < (when.month, when.day)
        return on.year - when.year - was_earlier

    @date_derniere_revision.setter
    def date_derniere_revision(self, valeur):
        self._date_derniere_revision = valeur

    def __str__(self):
        return "{} {} - {} - Config {} : {}F/{}C/{}P/{}Y ({} pax) - " \
               "Age : {} ans (premier vol : {}, derniere revision : {})"\
            .format(self._compagnie.id_code_iata, self._id,
                    self._config.type_avion, self._config.nom,
                    self._config.nb_place_premiere,
                    self._config.nb_place_business,
                    self._config.nb_place_eco_plus,
                    self._config.nb_place_eco,
                    self._config.nb_total_place,
                    self.age, self._date_construction,
                    self._date_derniere_revision)
