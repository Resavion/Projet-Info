class Compagnie(object):
    def __init__(self,  id_compagnie, nom_compagnie, alias, iata, icao, callsign, pays, actif):
        """
        Constructeur de la classe compagnie
        
        :param id_compagnie: identifiant de la compagnie
        :param nom_compagnie: nom de la compagnie
        :param alias: alias de la compagnie
        :param iata: code iata de la compagnie
        :param icao: code icao de la compagnie
        :param callsign: callsigne de la compagnie
        :param pays: pays d'origine de la compagnie
        :param actif: si la compagnie est toujours active
        """

        self._id_compagnie = id_compagnie
        self._nom_compagnie = nom_compagnie
        self._alias = alias
        self._iata = iata
        self._icao = icao
        self._callsign = callsign
        self._pays = pays
        self._actif= actif

    