class Segment(object):
    def __init__(self, id_segment, billet, vol, horaire_codeshare,
                 place, options):
        """
        Constructeur de la classe segment
        
        :param id_segment: identifiant du segment
        :param billet: billet qui contient ce segment
        :param vol: vol concerne par ce segment
        :param horaire_codeshare: horaire concerne par ce segment si codeshare
        :param place: numero du siège
        :param options: options que le passager a pris pour cette partie de trajet
        """
        self._id = id_segment
        self._billet = billet
        self._vol = vol
        self._horaire = vol.horaire
        if horaire_codeshare is not None:
            self._horaire = horaire_codeshare
        self._place = place
        self._options = options

    @property
    def id(self):
        return self._id

    @property
    def billet(self):
        return self._billet

    @property
    def vol(self):
        return self._vol

    @property
    def horaire(self):
        return self._horaire

    @property
    def place(self):
        return self._place

    @property
    def options(self):
        return self._options

    def __str__(self):
        txt = "Vol {} {}{:4s} - {} -> {} - {:%d/%m/%Y %H:%M} -> {:%d/%m/%Y %H:%M} - Siège {} - {} {}"\
            .format(self._horaire.compagnie.code_icao,
                    self._horaire.compagnie.id_code_iata,
                    str(self._horaire.numero),
                    self._horaire.route.aeroport_depart.id_code_iata,
                    self._horaire.route.aeroport_arrivee.id_code_iata,
                    self._vol.datetime_depart,
                    self._vol.datetime_arrivee,
                    self._place,
                    self._billet.nom_passager.upper(),
                    self._billet.prenom_passager.upper())
        if self._vol.horaire != self._horaire:
            txt = txt + " - Vol assuré par {}".format(self._vol.horaire.compagnie.nom)
        return txt

    def modifier_place(self):
        """
        Methode qui permet de modifier la place du passager
        :return: 
        """
        pass

    def modifier_options(self):
        """
        Methode qui permet de modifier les options choisies pour le segment
        
        :return: 
        """
        pass



