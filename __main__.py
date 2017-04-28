import os

from bdd.config_bdd import creer_bdd
from reservation.utilitaire import charger_bd


if __name__ == '__main__':
    db_name = "bdd/resavion.db"
    if not os.path.exists(db_name):
        creer_bdd(db_name)

    charger_bd(db_name)

    #
    # joueur, dresseurs, pokemons_sauvages = charger_partie(db_name)
    #
    # if joueur is None:
    #     joueur = initialiser_partie(db_name)
    #
    # jouer(joueur, dresseurs, pokemons_sauvages)
    #
    # sauvegarder_partie(db_name, joueur)








