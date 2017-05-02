from enum import Enum


class EnumAvion(Enum):
    EN_REVISION = 1
    EN_VOL = 2
    AU_SOL = 3


class EnumOption(Enum):
    VEGETARIEN = 1
    ASSURANCE_ANNULATION = 2


class EnumStatutVol(Enum):
    A_L_HEURE = 1
    RETARDE = 2
    EMBARQUEMENT = 3
    ANNULE = 4
    ARRIVE = 5
