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
        new_colon = ihm.demander(
            "Saisissez la colonne:")
        self.vol.cabine.liberer_place(self, old_rangee, old_colonne)
        self.vol.cabine.reserver_place(self, new_rangee, new_colonne)

        new_place = (new_rang,new_colonne)
        self._billet = "".join(new_place)

    def modifier_options(self):
        """
        Methode qui permet de modifier les options choisies pour le segment
        
        :return: 
        """
        pass

if __name__=='__main__':
    avion = """  ABC DEFG HJK
  ------------
 |>          <|
 |>   ----   <|
F|.-- O--O --O|1
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

    def reserver_place(avion, rangee, colonne, F = 7, C = 52, P=24, Y = 180):
        """
        Methode qui permet de reserver une place dans un vol en changeant le signe de 
        la place "O" en "." pour l'affichage.
        Elle met à jour le nombre de place selon la classe
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


    def liberer_place(avion, rangee, colonne, F = 7, C = 52, P=24, Y = 180):
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
                    drapeau[colonne] = "O"
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

    def modifier_place(avion, old_rangee, old_colonne,new_rangee, new_colonne):
        """
        Methode qui permet de modifier la place du passager
        :return: 
        """
        avion1 = liberer_place(avion, old_rangee, old_colonne)
        print(avion1)
        avion2 = reserver_place(avion1, new_rangee, new_colonne)
        print(avion2)
        #self.vol.cabine.liberer_place(self, old_rangee, old_colonne)
        #self.vol.cabine.reserver_place(self, new_rangee, new_colonne)


    #modifier_place(avion,1,'A',42,'G')




