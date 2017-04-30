

class Reservation(object):
    def __init__(self, id, client, prix_total, date_achat,
                 billets=None):
        """
        Constructeur de la classe reservation
        
        :param id: identifiant de la reservation
        :param client: client qui a fait la reservation
        :param prix_total: prix total à payer pour la reservation
        :param date_achat: date de paiement de la reservation
        :param billets: billets concernes par cette reservation
        """
        self._id = id
        self._client = client
        self._prix_total = prix_total
        self._date_achat = date_achat
        if billets is None:
            billets = []
        self._billets = billets

    @property
    def id(self):
        return self._id

    @property
    def client(self):
        return self._client

    @property
    def prix_tota(self):
        return self._prix_total

    @property
    def date_achat(self):
        return self._date_achat

    @property
    def billets(self):
        return self._billets

    def __str__(self):
        return "Réservation n°{:05d} - Par : {}, {} - Total : {} € - " \
               "Le : {:%d/%m/%Y à %Hh%M}"\
            .format(self._id,
                    self._client.nom, self._client.prenom,
                    self._prix_total, self._date_achat)

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

    def fournir_recapitulatif(self):
        """
        Methode qui permet de fournir au client le recapitulatif de sa reservation
        :return: 
        """
        pass

