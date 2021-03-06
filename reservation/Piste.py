class Piste(object):
    def __init__(self, id_piste, aeroport, length_ft, le_identificateur, le_seuil_decale_ft,
                 he_identificateur, he_seuil_decale_ft):
        """
        Constructeur de la classe Piste
        
        :param id_piste: identifiant de la piste
        :param aeroport: aeroport auquel appartient la piste
        :param length_ft: longueur de la piste en feet 
        :param le_identificateur: identifiant de la piste sur l'extremite 1
        :param le_seuil_decale_ft: le seuil decale de la piste 1
        :param he_identificateur: identifiant de la piste sur l'extremite 2
        :param he_seuil_decale_ft: le seuil decale de la piste 2
        """
        self._id                 = id_piste
        self._aeroport           = aeroport
        self._length_ft          = length_ft
        self._le_identificateur  = le_identificateur
        self._le_seuil_decale_ft = le_seuil_decale_ft
        self._he_identificateur  = he_identificateur
        self._he_seuil_decale_ft = he_seuil_decale_ft

    @property
    def id(self):
        return self._id

    @property
    def aeroport(self):
        return self._aeroport

    @property
    def length_ft(self):
        return self._length_ft

    @property
    def le_identificateur(self):
        return self._le_identificateur

    @property
    def le_seuil_decale_ft(self):
        return self._le_seuil_decale_ft

    @property
    def he_identificateur(self):
        return self._he_identificateur

    @property
    def he_seuil_decale_ft(self):
        return self._he_seuil_decale_ft

    def __str__(self):
        return "{} - {}/{} ({} ft)".format(self._aeroport, self._le_identificateur,
                                           self._he_identificateur, self._length_ft)





