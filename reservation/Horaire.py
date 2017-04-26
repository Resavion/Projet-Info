class Horaire(object):
    def __init__(self, id_compagnie, numero, route, heure_depart, heure_arrivee, duree, periodicite, horaire_operateur, type_avion):
        """
        Constructeur de la classe horaire
        
        :param id_compagnie: 
        :param numero: 
        :param route: 
        :param heure_depart: 
        :param heure_arrivee: 
        :param duree: 
        :param periodicite: 
        :param horaire_operateur: 
        :param type_avion: 
        """


        self._id_compagnie = id_compagnie
        self._numero = numero
        self._route = route
        self._heure_depart = heure_depart
        self._heure_arrivee = heure_arrivee
        self._duree = duree
        self._periodicite = periodicite
        self._horaire_operateur = horaire_operateur
        self._type_avion = type_avion

    @property
    def id_compagnie(self):
        return

    @property
    def numero(self):
        return

    @property
    def route(self):
        return
    def heure_depart(self):
        return

    @property
    def heure_arrivee(self):
        return

    @property
    def duree(self):
        return

    @property
    def periodicite(self):
        return

    @property
    def horaire_operateur(self):
        return

    @property
    def type_avion(self):
        return

    def creer_vols(self):
        """
        
        :return: 
        """
        pass

    def afficher_stats(self):
        """
        
        :return: 
        """
        pass