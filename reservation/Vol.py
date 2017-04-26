class Vol(object):
    def __init__(self, id_horaire, date, heure_depart, heure_arrivee, heure_embarquement, avion, places_restantes, statut):
        """
        Constructeur de la classe vol
        
        :param id_horaire: horaire du vol
        :param date: date du vol
        :param heure_depart: heure de depart du vol
        :param heure_arrivee: heure d'arrivee du vol
        :param heure_embarquement: heure d'embarquement calculé a partir de l'heure de depart et le nombre de place dans l'avion
        :param avion: type de l'avion qui fait le vol
        :param places_restantes: le nombre de places restantes dans le vol
        :param statut: statut indiquant l'etat du vol
        """
        self._id_horaire = id_horaire
        self._date = date
        self._heure_depart = heure_depart
        self._heure_arrivee = heure_arrivee
        self._heure_embarquement = heure_embarquement
        self._avion = avion
        self._places_restantes = places_restantes
        self._statut = statut

    @property
    def id_horaire(self):
        return self._id_horaire

    @property
    def date(self):
        return self._date

    @property
    def heure_depart(self):
        return self._heure_depart

    @property
    def heure_arrivee(self):
        return self._heure_arrivee

    @property
    def heure_embarquement(self):
        return self._heure_embarquement

    @property
    def avion(self):
        return self._avion

    @property
    def places_restantes(self):
        return self._places_restantes

    @property
    def statut(self):
        return self._statut


    def afficher_places(self):
        """
        Methode qui permet d'afficher les places disponibles et non disponibles dans un avion
        :return: 
        """
        pass

    def reserver_place(self):
        """
        Methode qui permet de reserver un place dans un vol
        :return: 
        """
        pass

    def liberer_place(self):
        """
        Methode qui permet de liberer une place dans un vol
        :return: 
        """
        pass

    def retarder_vol(self):
        """
        Methode qui permet de retarder l'heure de depart du vol
        :return: 
        """
        pass

    def modifier_position_avion(self):
        """
        Methode qui permet de modifier la position de l'avion en fonction de ses coordonnées
        
        :return: 
        """
        pass

    def annuler_vol(self):
        """
        Methode qui permet d'annuler le vol
        
        :return: 
        """
        pass

