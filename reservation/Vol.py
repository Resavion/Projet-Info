class Vol(object):
    def __init__(self, id_vol, horaire, datetime_depart, datetime_arrivee, duree, avion,
                 places_restantes_premiere, places_restantes_business, places_restantes_eco_plus,
                 places_restantes_eco, statut, cabine=None):
        """
        Constructeur de la classe vol

        :param id_vol: id du vol
        :param horaire: horaire du vol
        :param datetime_depart: date et heure de depart du vol
        :param datetime_arrivee: date et heure d'arrivee du vol
        :param duree: duree du vol
        :param avion: avion qui fait le vol
        :param places_restantes_premiere: le nombre de places premiere restantes dans le vol
        :param places_restantes_business: le nombre de places business restantes dans le vol
        :param places_restantes_eco_plus: le nombre de places eco_plus restantes dans le vol
        :param places_restantes_eco: le nombre de places eco restantes dans le vol
        :param statut: statut indiquant l'etat du vol
        :param cabine: schema des places du vol
        """
        self._id = id_vol
        self._horaire = horaire
        self._datetime_depart = datetime_depart
        self._datetime_arrivee = datetime_arrivee
        self._duree = duree
        self._avion = avion
        self._places_restantes_premiere = places_restantes_premiere
        self._places_restantes_business = places_restantes_business
        self._places_restantes_eco_plus = places_restantes_eco_plus
        self._places_restantes_eco = places_restantes_eco
        self._statut = statut
        self._cabine = cabine
        if cabine is None:
            self._cabine = horaire.config_avion.disposition

    @property
    def id(self):
        return self._id

    @property
    def horaire(self):
        return self._horaire

    @property
    def datetime_depart(self):
        return self._datetime_depart

    @property
    def datetime_arrivee(self):
        return self._datetime_arrivee

    @property
    def duree(self):
        return self._duree

    @property
    def heure_embarquement(self):
        return None

    @property
    def avion(self):
        return self._avion

    @property
    def places_restantes_premiere(self):
        return self._places_restantes_premiere

    @property
    def places_restantes_business(self):
        return self._places_restantes_business

    @property
    def places_restantes_eco_plus(self):
        return self._places_restantes_eco_plus

    @property
    def places_restantes_eco(self):
        return self._places_restantes_eco

    @property
    def statut(self):
        return self._statut

    @property
    def cabine(self):
        return self._cabine

    def __str__(self):
        txt = "Vol {} {} {}{} - {} -> {} - {:%d/%m/%Y %H:%M} -> {:%d/%m/%Y %H:%M}".\
            format(self._id,
                   self._horaire.compagnie.code_icao,
                   self._horaire.compagnie.id_code_iata, self._horaire.numero,
                   self._horaire.route.aeroport_depart.id_code_iata,
                   self._horaire.route.aeroport_arrivee.id_code_iata,
                   self._datetime_depart,
                   self._datetime_arrivee)
        if self._avion is not None:
            txt += " - {}".format(self._avion.config.type_avion)
        return txt

    def afficher_places(self):
        """
        Methode qui permet d'afficher les places disponibles et non disponibles dans un avion
        :return: 
        """
        pass

    def reserver_place(self,avion): # rang, colonne):
        """
        Methode qui permet de reserver une place dans un vol
        :return: 
        """
        rangs = avion
        for rang in rangs.split("\n"):
            print(rang)

        #"""accroché a une chaine de caractere"""".replace("l","L")



    def liberer_place(self):
        """
        Methode qui permet de liberer une place dans un vol
        :return: 
        """
        pass

    def retarder_vol(self):
        """
        Methode qui permet de retarder l'heure de depart du vol
        :return: 
        """
        pass

    def modifier_position_avion(self):
        """
        Methode qui permet de modifier la position de l'avion en fonction de ses coordonnées
        
        :return: 
        """
        pass

    def annuler_vol(self):
        """
        Methode qui permet d'annuler le vol
        
        :return: 
        """
        pass

if __name__=='__main__':
    avion = """  ABC DEFG HJK
  ------------
 |>          <|
 |>   ----   <|
F|O-- O--O --O|1
F|O-- O--O --O|2
 |--- ---- ---|
C|O-- O-O- O--|5
C|--O -O-O --O|6
 |--- ---- ---|
C|O-- O-O- O--|7
C|--O -O-O --O|8
C|O-- O-O- O--|9
C|--O -O-O --O|10
C|O-- O-O- O--|11
C|--O -O-O --O|12
C|O-- O-O- O--|13
C|--O -O-O --O|14
C|O-- O-O- O--|15
C|--O -O-O --O|16
C|O-- O-O- O--|17
 |>          <|
 |>   ----   <|
P|O-O OOOO O-O|18
P|O-O OOOO O-O|19
P|O-O OOOO O-O|20
 |--- ---- ---|
Y|OOO OOOO OOO|24
Y|OOO OOOO OOO|25
Y|OOO OOOO OOO|26
Y|OOO OOOO OOO|27
Y|OOO OOOO OOO|28
Y|OOO OOOO OOO|29
 |>          <|
 |>   ----   <|
Y|OOO OOOO OOO|30
Y|OOO OOOO OOO|31
Y|OOO OOOO OOO|32
Y|OOO OOOO OOO|33
Y|OOO OOOO OOO|34
Y|OOO OOOO OOO|35
Y|OOO OOOO OOO|36
Y|OOO OOOO OOO|37
Y|OOO OOOO OOO|38
Y|OO  OOOO  OO|39
Y|OO  OOOO  OO|40
Y|OO  OOOO  OO|41
Y|OO  OOOO  --|42
 |>   ----   <|
 |>          <|
  ------------"""
    #print(avion)

    def reserver_place(avion, rangee, colonne):
        """
        Methode qui permet de reserver une place dans un vol
        :return: 
        """
        rangee = rangee - 1
        rangs = avion
        #for rang in rangs.split("\n"):
        #print(rangs.split("\n")[rangee])
        list_rang = rangs.split("\n")
        colonne = list_rang[0].index(colonne) - 2

        classe_rg5 = list_rang[5].split("|")[0]
        classe_rga = list_rang[0].split("|")[0]
        body_rg5 = list_rang[5].split("|")[1]
        num_rg5 = list_rang[5].split("|")[2]
     #   print(classe_rg5)
  #      print(classe_rga)
   #     print(body_rg5)
   #     print(num_rg5)
        for rang in list_rang[2:-1]:
            num_rg = rang.split("|")[2]
            body_rg = rang.split("|")[1]
            if num_rg == str(rangee+1):
                 # print (body_rg[colonne])
                if body_rg[colonne] == "O":
                    drapeau = list(body_rg)
                    drapeau[colonne]="."
                    body_rg = "".join(drapeau)
                    print(body_rg)

        # reassembler tous les elements

            # """accroché a une chaine de caractere"""".replace("l","L")







  #  body_rg = rang.split("|")[1]
   # if num_rg == rangee:
    #    print(body_rg)

    reserver_place(avion,1,'A')






