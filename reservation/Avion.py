class Avion(object):
    def __init__(self, id_avion, id_compagnie, config, date_construction, date_derniere_revision, 
                 etat, id_aeroport, position):
        """
        Constructeur de la classe avion
        
        :param id_avion: identifiant avion
        :param id_compagnie: id de la compagnie qui possède l'avion
        :param config: configuration de l'avion
        :param date_construction: date de construction de l'avion
        :param date_derniere_revision: derniere date de revision de l'avion
        :param etat: donne l'etat de l'avion, si il est en vol, au sol, non utilisable
        :param id_aeroport: l'id de l'aeroport ou il se situe actuellement
        :param position: la position de l'avion en fonction de ses coordonnées
        """
        self._id_avion = id_avion
        self._id_compagnie = id_compagnie
        self._config = config
        self._date_construction = date_construction
        self._date_derniere_revision = date_derniere_revision
        self._etat = etat
        self._id_aeroport = id_aeroport
        self._position = position

    @property
    def id_avion(self):
        return self._id_avion

    @property
    def id_compagnie(self):
        return self._id_compagnie

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
    def id_aeroport(self):
        return self._id_aeroport

    @property
    def position(self):
        return self._position

    def __str__(self):
        return "{} {} ({}/{}-{} pax) - {}".format(self._id_compagnie,self._id_avion,
                                                    self._config.type_avion,self._config.nom,
                                                    self._config.nb_total_place,
                                                    self._date_construction)