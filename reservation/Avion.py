class Avion(object):
    def __init__(self, id_avion, date_construction, date_derniere_revision, etat, aeroport, compagnie, typeAvion, date_prochaine_revision, aeroport_actuel, position, statut):
        """
        Constructeur de la classe avion
        
        :param id_avion: 
        :param date_construction: 
        :param date_derniere_revision: 
        :param etat: 
        :param aeroport: 
        :param compagnie: 
        :param typeAvion: 
        :param date_prochaine_revision: 
        :param aeroport_actuel: 
        :param position: 
        :param statut: 
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