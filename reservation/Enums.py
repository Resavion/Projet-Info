from enum import Enum


class EnumMere(Enum):
    def __str__(self):
        txt = "{}".format(self.name)
        txt = txt.replace("_"," ")
        txt = txt.replace("1","'")
        txt = txt.lower().capitalize()
        return txt


class EnumAvion(EnumMere):
    EN_REVISION = 1
    EN_VOL      = 2
    AU_SOL      = 3


class EnumOption(EnumMere):
    VEGETARIEN           = 1
    ASSURANCE_ANNULATION = 2


class EnumStatutVol(EnumMere):
    A_L_HEURE    = 1
    RETARDE      = 2
    EMBARQUEMENT = 3
    ANNULE       = 4
    ARRIVE       = 5
