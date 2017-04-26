class Client(object):
    def __init__(self, id_client, nom, prenom, date_naissance):
        """
        Constructeur de la classe client
        
        :param id_client: identifiant du compte client 
        :param nom: nom du client
        :param prenom: prenom du client
        :param date_naissance: date de naissance du client
        """

        self._id_client = id_client
        self._nom = nom
        self._prenom = prenom
        self._date_naissance = date_naissance

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

