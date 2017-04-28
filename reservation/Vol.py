import reservation.Horaire
import reservation.ConfigAvion


class Vol(object):
    def __init__(self, horaire, date, heure_depart, heure_arrivee, decalage_jour, avion,
                 places_restantes_premiere, places_restantes_business, places_restantes_eco_plus,
                 places_restantes_eco, statut):
        """
        Constructeur de la classe vol
        
        :param horaire: horaire du vol
        :param date: date du vol
        :param heure_depart: heure de depart du vol
        :param heure_arrivee: heure d'arrivee du vol
        :param decalage_jour: vaut 1 si l'heure d'arrivée est dans le jour suivant
        :param avion: type de l'avion qui fait le vol
        :param places_restantes_premiere: le nombre de places premiere restantes dans le vol
        :param places_restantes_business: le nombre de places business restantes dans le vol
        :param places_restantes_eco_plus: le nombre de places eco_plus restantes dans le vol
        :param places_restantes_eco: le nombre de places eco restantes dans le vol
        :param statut: statut indiquant l'etat du vol
        """
        self._horaire = horaire
        self._date = date
        self._heure_depart = heure_depart
        self._heure_arrivee = heure_arrivee
        self._decalage_jour = decalage_jour
        self._avion = avion
        self._places_restantes_premiere = places_restantes_premiere
        self._places_restantes_business = places_restantes_business
        self._places_restantes_eco_plus = places_restantes_eco_plus
        self._places_restantes_eco = places_restantes_eco
        self._statut = statut
        self._cabine = horaire.config_avion.disposition

    @property
    def horaire(self):
        return self._horaire

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
        return None

    @property
    def avion(self):
        return self._avion

    @property
    def places_restantes_premiere(self):
        return self._places_restantes_premiere

    @property
    def places_restantes_business(self):
        return self._places_restantes_business

    @property
    def places_restantes_eco_plus(self):
        return self._places_restantes_eco_plus

    @property
    def places_restantes_eco(self):
        return self._places_restantes_eco

    @property
    def statut(self):
        return self._statut

    @property
    def cabine(self):
        return self._cabine

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

