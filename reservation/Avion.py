class Avion(object):
    def __init__(self, id_avion, date_construction, date_derniere_revision, etat, aeroport, compagnie, typeAvion,
                 date_prochaine_revision, aeroport_actuel, position, statut):
        """
        Constructeur de la classe avion
        
        :param id_avion: identifiant avion
        :param date_construction: date de construction de l'avion
        :param date_derniere_revision: derniere date de revision de l'avion
        :param etat: donne l'etat de l'avion, si il est en vol, au sol, non utilisable
        :param compagnie: la compagnie a laquelle il appartient
        :param typeAvion: le type de l'avion
        :param date_prochaine_revision: la date de la prochaine revision en fonction de la premiere
        :param aeroport_actuel: l'aeroport ou il se situe actuellement
        :param position: la position de l'avion en fonction de ses coordonnées
        """
        self._id_avion = id_avion
        self._date_construction = date_construction
        self._date_derniere_revision = date_derniere_revision
        self._etat = etat
        self._aeroport = aeroport
        self._compagnie = compagnie
        self._typeAvion = typeAvion
        self._date_prochaine_revision = date_prochaine_revision
        self._aeroport_actuel = aeroport_actuel
        self._position = position
        self._statut = statut


    @property
    def id_avion(self):
        return self._id_avion

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
    def compagnie(self):
        return self._compagnie

    @property
    def typeAvion(self):
        return self._typeAvion

    @property
    def date_prochaine_revision(self):
        return self._date_prochaine_revision

    @property
    def aeroport_actuel(self):
        return self._aeroport_actuel

    @property
    def position(self):
        return self._position

    @property
    def statut(self):
        return self._statut