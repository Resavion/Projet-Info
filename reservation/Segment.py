from reservation.Vol import Vol
import ihm.console as ihm

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
        self._id      = id_segment
        self._billet  = billet
        self._vol     = vol
        self._horaire = vol.horaire
        if horaire_codeshare is not None:
            self._horaire = horaire_codeshare
        self._place   = place
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
        txt = "Segment {} {}{:4s} - {} -> {} - {:%d/%m/%Y %H:%M} -> {:%d/%m/%Y %H:%M} - Siège {} - {} {}"\
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
        Methode qui permet de modifier la place du passager en lui demandant la nouvelle place voulue
        et de changer la place sur le billet
        :return: 
        """

        # on stocke l'ancien rang et l'ancienne colonne
        old_rangee = int(self._place[0:-1])
        old_colonne = int(self._place[-1])

        # on demande le nouveau rang et la nouvelle colonne
        new_rang = ihm.demander(
            "Saisissez le rang:")
        new_rangee = int(new_rang)
        new_colonne = ihm.demander(
            "Saisissez la colonne:")
        self.vol.liberer_place(old_rangee, old_colonne)
        self.vol.reserver_place(new_rangee, new_colonne)

        new_place = (new_rang,new_colonne)
        self._place = "".join(new_place)

    def modifier_options(self):
        """
        Methode qui permet de modifier les options choisies pour le segment
        
        :return: 
        """
        pass





