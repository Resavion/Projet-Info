class Horaire(object):
    def __init__(self, id_compagnie, numero, route, heure_depart, heure_arrivee, duree, periodicite, id_horaire_operateur,
                 type_avion):
        """
        Constructeur de la classe horaire
        
        :param id_compagnie: identifiant de la compagnie
        :param numero: numero de vol 
        :param route: route empruntée par le vol
        :param heure_depart: heure de depart du vol
        :param heure_arrivee: heure d'arrivee du vol
        :param duree: duree du vol
        :param periodicite: nombre de fois ou se vole est effectue (par semaine, mois, annee, saison...)
        :param id_horaire_operateur: identifiant de l'horaire de la compagnie qui va operer le vol
        :param type_avion: le type d'avion utilisé a cette horaire
        """


        self._id_compagnie = id_compagnie
        self._numero = numero
        self._route = route
        self._heure_depart = heure_depart
        self._heure_arrivee = heure_arrivee
        self._duree = duree
        self._periodicite = periodicite
        self._id_horaire_operateur = id_horaire_operateur
        self._type_avion = type_avion

    @property
    def id_compagnie(self):
        return self._id_compagnie

    @property
    def numero(self):
        return self._numero

    @property
    def route(self):
        return self._route

    def heure_depart(self):
        return self._heure_depart

    @property
    def heure_arrivee(self):
        return self._heure_arrivee

    @property
    def duree(self):
        return self._duree

    @property
    def periodicite(self):
        return self._periodicite

    @property
    def id_horaire_operateur(self):
        return self._id_horaire_operateur

    @property
    def type_avion(self):
        return self._type_avion

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