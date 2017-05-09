from reservation.Segment import Segment
from reservation.Billet import Billet


class Reservation(object):
    def __init__(self, id_resa, client, prix_total, date_achat,
                 billets=None):
        """
        Constructeur de la classe reservation
        
        :param id_resa: identifiant de la reservation
        :param client: client qui a fait la reservation
        :param prix_total: prix total à payer pour la reservation
        :param date_achat: date de paiement de la reservation
        :param billets: billets concernes par cette reservation
        """
        self._id         = id_resa
        self._client     = client
        self._prix_total = prix_total
        self._date_achat = date_achat
        if billets is None:
            billets   = []
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
        return "Id : {:05d} - Par : {}, {} - Total : {} € - " \
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
        # HYP on part du principe que chaque passager a les memes segments

        for billet in self._billets:
            print("VOTRE ITINERAIRE\n\n"
                  "DATE D'ENVOI DE L'ITINERAIRE: {}\n"
                  "PASSAGER : {} {} (DATE DE NAISSANCE {:%d/%m/%Y})\n"
                  "PASSPORT : {} \n"
                  "REFERENCE DE DOSSIER: {} \n"
                  \
                  .format(self._date_achat,
                          billet.nom_passager.upper(),
                          billet.prenom_passager.upper(),
                          billet.date_naissance,
                          billet.passeport,
                          self._id) )
            for segment in billet.segments:
                print("VOL:  {} {}{:4s} - {}     {} {} A {} {}      {:%d/%m/%Y}\n"
                      "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n\n"

                      "DEPART:  {:%d/%m/%Y %H:%M} - {}, {} ({})\n"
                      "ARRIVEE: {:%d/%m/%Y %H:%M} - {}, {} ({})\n"
                      "_  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _\n"
                      "CLASSE: ICI ca serait bien d'avoir la classe de la place ?\n"
                      "NON FUMEUR\n"
                      "DUREE: {}h{:02d}\n"
                      "EQUIPEMENT: {} - {}\n"
                      "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
                      "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n\n"\
                      .format(segment.horaire.compagnie.code_icao,
                              segment.horaire.compagnie.id_code_iata,
                              str(segment.horaire.numero),
                              segment.vol.horaire.compagnie.nom,
                              segment.horaire.route.aeroport_depart.municipalite.upper(),
                              segment.horaire.route.aeroport_depart.code_pays.upper(),
                              segment.horaire.route.aeroport_arrivee.municipalite.upper(),
                              segment.horaire.route.aeroport_arrivee.code_pays.upper(),
                              segment.vol.datetime_depart,
                              segment.vol.datetime_depart,
                              segment.horaire.route.aeroport_depart.municipalite.upper(),
                              segment.horaire.route.aeroport_depart.nom.upper(),
                              segment.horaire.route.aeroport_depart.id_code_iata,
                              segment.vol.datetime_arrivee,
                              segment.horaire.route.aeroport_arrivee.municipalite.upper(),
                              segment.horaire.route.aeroport_arrivee.nom.upper(),
                              segment.horaire.route.aeroport_arrivee.id_code_iata,
                              segment.vol.duree.seconds // 3600,
                              (segment.vol.duree.seconds // 60) % 60,
                              segment.vol.horaire.compagnie.id_code_iata,
                              segment.vol.horaire.config_avion.type_avion) )
        return


