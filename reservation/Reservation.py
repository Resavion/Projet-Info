

class Reservation(object):
    def __init__(self, id_reservation, id_client, prix_total, date_achat):
        """
        Constructeur de la classe reservation
        
        :param id_reservation: numero de la reservation
        :param id_client: identifiant du client qui a fait la reservation
        :param prix_total: prix total à payer pour la reservation
        :param date_achat: date de paiement de la reservation
        """

        self._id_reservation = id_reservation
        self._id_client = id_client
        self._prix_total = prix_total
        self._date_achat = date_achat

    def ajouter_billet(self):
        """
        Methode qui permet d'ajouter un billet à la reservation
        :return: 
        """
        pass

    def modifier_billet(self):
        """
        Methode qui permet de modifier un billet d'avion une fois avoir été ajouté
        :return: 
        """

    def supprimer_billet(self):
        """
        Methode pour supprimer un billet d'avion de la reservation une fois crée
        :return: 
        """
        pass

