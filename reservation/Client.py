class Client(object):
    def __init__(self, id_client, nom, prenom, date_naissance,
                 reservations=None):
        """
        Constructeur de la classe client
        
        :param id_client: identifiant du compte client 
        :param nom: nom du client
        :param prenom: prenom du client
        :param date_naissance: date de naissance du client
        :param reservations: liste des reservations du client
        """
        self._id = id_client
        self._nom = nom
        self._prenom = prenom
        self._date_naissance = date_naissance
        if reservations is None:
            reservations = []
        self._reservations = reservations

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def date_naissance(self):
        return self._date_naissance

    @property
    def reservations(self):
        return self._reservations

    def __str__(self):
        return "{:3d} {}, {} ({:%d/%m/%Y})"\
            .format(self._id, self._nom, self._prenom, self._date_naissance)

    def faire_reservation(self):
        """
        Methode qui consiste a faire une reservation
        (saisir_critere, afficher_vols, choisir_vols, saisir_passager, payer..)
        :return: 
        """
        pass

    def consulter_reservation(self):
        """
        Methode qui permet d'afficher la reservation au client avec les différentes informations pour le vol
        :return: 
        """
        pass

    def modifier_reservation(self):
        """
        Methode qui permet de modifier la reservation (date, vol etc)
        :return: 
        """
        pass

    def supprimer_reservation(self):
        """
        Methode qui permet de supprimer la reservation
        :return: 
        """
        pass

