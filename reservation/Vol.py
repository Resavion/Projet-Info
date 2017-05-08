from collections import defaultdict


class Vol(object):
    cle_index = defaultdict()

    def __init__(self, horaire, datetime_depart, datetime_arrivee, duree, avion,
                 places_restantes_premiere, places_restantes_business, places_restantes_eco_plus,
                 places_restantes_eco, statut, cabine=None, segments=None):
        """
        Constructeur de la classe vol

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
        :param segments: segments de billets concernant ce vol
        """
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
        if cabine is None:
            cabine = horaire.config_avion.disposition
        self._cabine = cabine
        if segments is None:
            segments = []
        self._segments = segments
        cle = "{}{}{}".format(horaire.compagnie.id_code_iata,
                              horaire.numero,
                              datetime_depart)
        Vol.cle_index[cle] = self

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

    @property
    def segments(self):
        return self._segments

    def __str__(self):
        txt = "Vol {} {}{} - {} -> {} - {:%d/%m/%Y %H:%M} -> {:%d/%m/%Y %H:%M} - " \
              "Places restantes : F:{}/{} C:{}/{} P:{}/{} Y:{}/{}"\
            .format(self._horaire.compagnie.code_icao,
                    self._horaire.compagnie.id_code_iata,
                    self._horaire.numero,
                    self._horaire.route.aeroport_depart.id_code_iata,
                    self._horaire.route.aeroport_arrivee.id_code_iata,
                    self._datetime_depart,
                    self._datetime_arrivee,
                    self._places_restantes_premiere,
                    self._horaire.config_avion.nb_places_premiere,
                    self._places_restantes_business,
                    self._horaire.config_avion.nb_places_business,
                    self._places_restantes_eco_plus,
                    self._horaire.config_avion.nb_places_eco_plus,
                    self._places_restantes_eco,
                    self._horaire.config_avion.nb_places_eco)
        if self._avion is not None:
            txt += " - {}".format(self._avion.config.type_avion)
        return txt

    def afficher_places(self):
        """
        Methode qui permet d'afficher les places disponibles et non disponibles dans un avion
        :return: 
        """
        print(self._cabine)

    def reserver_place(self, rangee, colonne):
        """
        Methode qui permet de reserver une place dans un vol en changeant le signe de 
        la place "O" en "." pour l'affichage.
        Elle met à jour le nombre de place selon la classe
        :return: 
        """

        rangee = rangee - 1
        rangs = avion
        list_rang = rangs.split("\n")
        # on recupere l'indice de la colonne
        colonne = list_rang[0].index(colonne) - 2
        # on cree une chaine de caractere vide pour reformer l'avion une fois la place changee
        avion_change = ""
        # on cree le debut de l'avion
        for rang in list_rang[0:2]:
            avion_change += rang + "\n"
        for rang in list_rang[2:-1]:
            # on recupere le numero du rang
            num_rg = rang.split("|")[2]
            # on recupere le corps de l'avion
            body_rg = rang.split("|")[1]
            # on recupere la classe du rang
            classe_rg = rang.split("|")[0]
            changement = False
            if num_rg == str(rangee + 1):
                # on teste si le client a choisi une place libre ou non
                if body_rg[colonne] == ".":
                    print('Cette place est déjà occupée.')
                elif body_rg[colonne] == "O":
                    # changement des places restantes
                    if classe_rg == "F":
                        self._places_restantes_premiere -= 1
                    elif classe_rg == "C":
                        self._places_restantes_business -= 1
                    elif classe_rg == "P":
                        self._places_restantes_eco_plus -= 1
                    elif classe_rg == "Y":
                        self._places_restantes_eco -= 1
                    # on change le "O" en "." pour la place donnée
                    drapeau = list(body_rg)
                    drapeau[colonne] = "."
                    # on regroupe tous les morceaux pour reformer l'avion
                    body_rg = "".join(drapeau)
                else:
                    pass
                rang_chang = (classe_rg, body_rg, num_rg)
                rang_chang = "|".join(rang_chang)
                changement = True
            if changement:
                avion_change += rang_chang + "\n"
            else:
                avion_change += rang + "\n"

        for rang in list_rang[-1]:
            avion_change += rang
        # on sauvegarde le nouvel avion
        self._cabine = avion_change




    def liberer_place(self, rangee, colonne):
        """
        Methode qui permet de liberer une place dans un vol en changeant le signe de 
        la place "." en "O" pour l'affichage.
        Elle met à jour le nombre de place selon la classe
        :return: 
        """

        rangee = rangee - 1
        rangs = avion
        list_rang = rangs.split("\n")
        # on recupere l'indice de la colonne
        colonne = list_rang[0].index(colonne) - 2
        # on cree une chaine de caractere vide pour reformer l'avion une fois la place changee
        avion_change = ""
        # on cree le debut de l'avion
        for rang in list_rang[0:2]:
            avion_change += rang + "\n"
        for rang in list_rang[2:-1]:
            # on recupere le numero du rang
            num_rg = rang.split("|")[2]
            # on recupere le corps de l'avion
            body_rg = rang.split("|")[1]
            # on recupere la classe du rang
            classe_rg = rang.split("|")[0]
            if num_rg == str(rangee + 1):
                if body_rg[colonne] == ".":
                    # changement des places restantes
                    if classe_rg == "F":
                        self._places_restantes_premiere += 1
                    elif classe_rg == "C":
                        self._places_restantes_business += 1

                    elif classe_rg == "P":
                        self._places_restantes_eco_plus += 1

                    elif classe_rg == "Y":
                        self._places_restantes_eco += 1
                    # on change le "." en "O" pour la place donnée
                    drapeau = list(body_rg)
                    drapeau[colonne] = "O"
                    # on regroupe tous les morceaux pour reformer l'avion
                    body_rg = "".join(drapeau)
                rang_chang = (classe_rg, body_rg, num_rg)
                rang_chang = "|".join(rang_chang)
                changement = True
            if changement:
                avion_change += rang_chang + "\n"
            else:
                avion_change += rang + "\n"
        for rang in list_rang[-1]:
            avion_change += rang
        # on sauvegarde le nouvel avion
        self._cabine = avion_change



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

    def reserver_place(avion, rangee, colonne,F,C,P,Y):
        """
        Methode qui permet de reserver une place dans un vol en changeant le signe de 
        la place "O" en "." pour l'affichage.
        Elle met à jour le nombre de place selon la classe
        :return: 
        """
        #print('F',F,'C',C,'P',P,'Y',Y)
        places_restantes_premiere = F
        places_restantes_business = C
        places_restantes_eco_plus = P
        places_restantes_eco = Y

        rangee = rangee - 1
        rangs = avion
        list_rang = rangs.split("\n")
        colonne = list_rang[0].index(colonne) - 2
        avion_change = ""
        for rang in list_rang[0:2]:
            avion_change+= rang + "\n"
        for rang in list_rang[2:-1]:
            num_rg = rang.split("|")[2]
            body_rg = rang.split("|")[1]
            classe_rg = rang.split("|")[0]
            changement = False
            if num_rg == str(rangee+1):
                if body_rg[colonne] == "O":
                    # changement des places restantes
                    if classe_rg == "F":
                        places_restantes_premiere -= 1
                        #self._places_restantes_premiere -= 1
                    elif classe_rg == "C":
                        places_restantes_business -= 1
                        #self._places_restantes_business -= 1

                    elif classe_rg == "P":
                        places_restantes_eco_plus -= 1
                        #self._places_restantes_eco_plus -= 1

                    elif classe_rg == "Y":
                        #self._places_restantes_eco -= 1
                        places_restantes_eco -= 1


                    drapeau = list(body_rg)
                    drapeau[colonne]="."
                    body_rg = "".join(drapeau)
                    print(body_rg)
                    print(classe_rg)
                rang_chang = (classe_rg, body_rg, num_rg)
                rang_chang = "|".join(rang_chang)
                changement = True
            if changement:
                avion_change += rang_chang + "\n"
            else:
                avion_change += rang + "\n"

        for rang in list_rang[-1]:
            avion_change += rang

        #self._cabine = avion_change

        print('F', places_restantes_premiere, 'C', places_restantes_business, 'P', places_restantes_eco_plus,
              'Y', places_restantes_eco)
        return avion_change



            # """accroché a une chaine de caractere"""".replace("l","L")

    print('CACA qui pue')
    avion1=reserver_place(avion,1,'A',8,52,24,180)
    print(avion1)


    def afficher_places(avion):
        """
        Methode qui permet d'afficher les places disponibles et non disponibles dans un avion
        :return: 
        """
        print(avion)

    print('CACA')
    #afficher_places(avion)

    def liberer_place(avion, rangee, colonne,F,C,P,Y):
        """
        Methode qui permet de liberer une place dans un vol
        :return: 
        """
        print('F',F,'C',C,'P',P,'Y',Y)
        places_restantes_premiere = F
        places_restantes_business = C
        places_restantes_eco_plus = P
        places_restantes_eco = Y

        rangee = rangee - 1
        rangs = avion
        list_rang = rangs.split("\n")
        colonne = list_rang[0].index(colonne) - 2
        avion_change = ""
        for rang in list_rang[0:2]:
            avion_change += rang + "\n"
        for rang in list_rang[2:-1]:
            num_rg = rang.split("|")[2]
            body_rg = rang.split("|")[1]
            classe_rg = rang.split("|")[0]
            changement = False
            if num_rg == str(rangee + 1):
                if body_rg[colonne] == ".":
                    # changement des places restantes
                    if classe_rg == "F":
                        places_restantes_premiere += 1
                        # self._places_restantes_premiere += 1
                    elif classe_rg == "C":
                        places_restantes_business += 1
                        # self._places_restantes_business += 1

                    elif classe_rg == "P":
                        places_restantes_eco_plus += 1
                        # self._places_restantes_eco_plus += 1

                    elif classe_rg == "Y":
                        # self._places_restantes_eco += 1
                        places_restantes_eco += 1

                    drapeau = list(body_rg)
                    drapeau[colonne] = "X"
                    body_rg = "".join(drapeau)
                    print(body_rg)
                    print(classe_rg)
                rang_chang = (classe_rg, body_rg, num_rg)
                rang_chang = "|".join(rang_chang)
                changement = True
            if changement:
                avion_change += rang_chang + "\n"
            else:
                avion_change += rang + "\n"
        for rang in list_rang[-1]:
            avion_change += rang

        # self._cabine = avion_change

        print('F', places_restantes_premiere, 'C', places_restantes_business, 'P', places_restantes_eco_plus,
              'Y', places_restantes_eco)
        return avion_change



    avion2 = liberer_place(avion1,1,'A',7,52,24,180)
    print('CACA2')
    print(avion2)






