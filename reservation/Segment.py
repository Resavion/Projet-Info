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
        self._id_segment = id_segment
        self._billet = billet
        self._vol = vol
        self._horaire = vol.horaire
        if horaire_codeshare is not None:
            self._horaire = horaire_codeshare
        self._place = place
        self._options = options

    def __str__(self):
        txt = "Vol {} {}{} - {} -> {} - {:%d/%m/%Y %H:%M} -> {:%d/%m/%Y %H:%M} - Place {} - {} {}"\
            .format(self._horaire.compagnie.code_icao,
                    self._horaire.compagnie.id_compagnie,
                    self._horaire.numero,
                    self._horaire.route.aeroport_depart.id_aeroport,
                    self._horaire.route.aeroport_arrivee.id_aeroport,
                    self._vol.datetime_depart,
                    self._vol.datetime_arrivee,
                    self._place,
                    self._billet.nom_passager.upper(),
                    self._billet.prenom_passager.upper())
        if self._vol.horaire != self._horaire:
            txt = txt + " - Vol assuré par {}".format(self._vol.horaire.compagnie.nom_compagnie)
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



