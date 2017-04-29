class Horaire(object):
    def __init__(self, id_horaire, id_route, id_compagnie, numero, heure_depart, heure_arrivee, duree, periodicite, horaire_operateur,
                 config_avion):
        """
        Constructeur de la classe horaire
        
        :param id_horaire: identifiant de l'horaire
        :param id_route: id de la route empruntee par le vol
        :param id_compagnie: id de la compagnie qui propose la route
        :param numero: numero de vol 
        :param heure_depart: heure de depart du vol
        :param heure_arrivee: heure d'arrivee du vol
        :param duree: duree du vol
        :param periodicite: nombre de fois ou ce vol est effectue (par semaine, mois, annee, saison...)
        :param horaire_operateur: horaire de la compagnie qui va operer le vol
        :param config_avion: la configuration d'avion utilisee a cet horaire
        """
        self._id_horaire = id_horaire
        self._id_route = id_route
        self._id_compagnie = id_compagnie
        self._numero = numero
        self._heure_depart = heure_depart
        self._heure_arrivee = heure_arrivee
        self._duree = duree
        self._periodicite = periodicite
        self._horaire_operateur = horaire_operateur
        self._config_avion = config_avion

    @property
    def id_horaire(self):
        return self._id_horaire

    @property
    def id_route(self):
        return self._id_route

    @property
    def id_compagnie(self):
        return self._id_compagnie

    @property
    def numero(self):
        return self._numero

    @property
    def heure_depart(self):
        if self._horaire_operateur is None:
            return self._heure_depart
        return self._horaire_operateur.heure_depart

    @property
    def heure_arrivee(self):
        if self._horaire_operateur is None:
            return self._heure_arrivee
        return self._horaire_operateur.heure_arrivee

    @property
    def duree(self):
        if self._horaire_operateur is None:
            return self._duree
        return self._horaire_operateur.duree

    @property
    def periodicite(self):
        if self._horaire_operateur is None:
            return self._periodicite
        return self._horaire_operateur.periodicite

    @property
    def horaire_operateur(self):
        return self._horaire_operateur

    @property
    def config_avion(self):
        if self._horaire_operateur is None:
            return self._config_avion
        return self._horaire_operateur.config_avion

    def __str__(self):
        return "{}{:4s} - {:%H:%M} -> {:%H:%M} ({}h{})"\
            .format(self._id_compagnie,str(self._numero),
                    self.heure_depart,self.heure_arrivee,
                    self.duree.seconds//3600,(self.duree.seconds//60) % 60)

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