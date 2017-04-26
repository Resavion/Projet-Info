class Route(object):
    def __init__(self,  id_compagnie, aeroport_depart, aeroport_arrivee, geom, distance, codeshare):
        """
        Constructeur de la classe route
        
        :param id_compagnie: identifiant de la compagnie
        :param aeroport_depart: aeroport de depart de la route
        :param aeroport_arrivee: aeroport d'arrivee de la route
        :param geom: coordonnées de l'aeroport de depart
        :param distance: distance separant les deux aeroports
        :param codeshare: booleen qui permet de savoir si un avion est partagé par plusieurs compagnies
        """

        self._id_compagnie = id_compagnie
        self._aeroport_depart = aeroport_depart
        self._aeroport_arrivee = aeroport_arrivee
        self._geom = geom
        self._distance = distance
        self._codeshare = codeshare

    @property
    def id_compagnie(self):
        return self._id_compagnie

    @property
    def aeroport_depart(self):
        return self._id_compagnie

    @property
    def aeroport_arrivee(self):
        return self._id_compagnie

    @property
    def geom(self):
        return self._id_compagnie

    @property
    def distance(self):
        return self._id_compagnie

    @property
    def codeshare(self):
        return self._id_compagnie

    def ajouter_horaire(self):
        """
        Methode qui permet d'ajouter un horaire de vol a une route 
        :return: 
        """
        pass

    def supprimer_horaire(self):
        """
        Methode qui permet de supprimer un horaire de vol a une route
        
        :return: 
        """
        pass

    def calculer_plan_vol(self):
        """
        Methode pour calculer le trajet de l'avion en fonction des zones autorisées
        :return: 
        """
        pass

    def afficher_stats(self):
        """
        Methode qui permet d'afficher les statistiques sur le nombre personnes ayant réellement empruntés le chemin par rapport
        au nombre de places offertes
        :return: 
        """
        pass

    def afficher_horaires(self):
        """
        Methode qui permet d'afficher les horaires ou cette route est empruntée
        
        :return: 
        """

    def afficher_route(self):
        """
        Methode qui permet d'afficher la route reliant deux aeroports
        :return: 
        """
        pass

    def afficher_plan_vol(self):
        """
        Methode qui permet d'afficher le plan de vol et les différents points de passages (????)
        de l'avion
        :return: 
        """
        pass

    