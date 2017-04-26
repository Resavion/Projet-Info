class Pays(object):
    def __init__(self, id_pays, code_pays, nom, continent, keywords):
        """
        Constructeur de la classe Pays
        
        :param id_pays: identifiant du pays
        :param code_pays: code du pays
        :param nom: nom du pays
        :param continent: continent où se trouve le pays
        :param keywords: mots qui ont un rapport avec le pays
        """
        self._id_pays = id_pays
        self._code_pays = code_pays
        self._nom = nom
        self._continent = continent
        self._keywords = keywords
        


