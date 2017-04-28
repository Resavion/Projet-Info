class Segment(object):
    def __init__(self, id_segment, id_billet, id_vol, place, options):
        """
        Constructeur de la classe segment
        
        :param id_segment: identifiant du segment
        :param id_billet: identifiant du billet
        :param id_vol: numero de vol
        :param place: numero du siège
        :param options: options que le passager a pris pour cette partie de trajet
        """
        self._id_segment = id_segment
        self._id_billet = id_billet
        self._id_vol = id_vol
        self._place = place
        self._options = options

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



