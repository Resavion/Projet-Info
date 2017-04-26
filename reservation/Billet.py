class Billet(object):
    def __init__(self, id_billet, id_reservation, tarif, nom_passager, prenom_passager, passeport, date_naissance, options):
        """
        Constructeur de la classe billet
        
        :param id_billet: identifiant du billet
        :param id_reservation: numero de reservation
        :param tarif: prix du billet
        :param nom_passager: nom du passager qui fait le vol
        :param prenom_passager: prenom du passager qui fait le vol
        :param passeport: passeport du passager faisant le vol
        :param date_naissance: date de naissance du passager faisant le vol
        :param options: options que le passager à pris pour son vol
        """
        self._id_billet = id_billet
        self._id_reservation = id_reservation
        self._tarif = tarif
        self._nom_passager = nom_passager
        self._prenom_passager = prenom_passager
        self._passeport = passeport
        self._date_naissance = date_naissance
        self._options = options


    @property
    def id_billet(self):
        return self._id_billet

    @property
    def id_reservation(self):
        return self._id_reservation

    @property
    def tarif(self):
        return self._tarif

    @property
    def nom_passager(self):
        return self._nom_passager

    @property
    def prenom_passager(self):
        return self._prenom_passager

    @property
    def passeport(self):
        return self._passeport

    @property
    def date_naissance(self):
        return self._date_naissance

    @property
    def options(self):
        return self._options


    def ajouter_segment(self):
        """
        Methode permettant de reserver une place dans un vol
        :return: 
        """
        pass

    def modifier_segment(self):
        """
        Methode permettant de modifier un segment de vol
        :return: 
        """
        pass

    def supprimer_segment(self):
        """
        Methode permettant de supprimer un segment de vol
        :return: 
        """
        pass


    def modifier_options(self):
        """
        Methode permettant de modifier les options choisies pour le vol
        :return: 
        """
        pass
