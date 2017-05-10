import os

import ihm.console as ihm
from bdd.config_bdd import (creer_bdd, inserer_jeu_test)
from utilitaires.chargement import (charger_bd,
                                    update_bd)
import utilitaires.menus as menus


if __name__ == '__main__':
    db_name = "bdd/resavion.db"
    if not os.path.exists(db_name):
        creer_bdd(db_name)
        inserer_jeu_test(db_name)

    aeroports, compagnies, clients = charger_bd(db_name)

    print('\n\n OHAYOOOOOOOOOOOOOOOOOOOO')

    from reservation.Aeroport import Aeroport
    aer_dep = Aeroport.find_by_id("HND")
    aer_arr = Aeroport.find_by_id("BKK")
    escales_max = 2
    classe = 'Y'
    combinaisons_total = []
    for compagnie in compagnies:
        combinaisons, combi_prix, combi_dist = compagnie.chercher_routes_escales(
            aer_dep, aer_arr, escales_max)
        if combinaisons:
            combinaisons_total.extend(zip(combinaisons, combi_prix, combi_dist))

    # # On lance l'interface
    # menus.menu_racine(clients, compagnies, aeroports)
    #
    # liste_choix = ('Oui', 'Non')
    # choix = ihm.choisir(liste_choix,
    #                     "Voulez-vous sauvegarder vos modifications ?")
    # if choix == 'Oui':
    #     update_bd(db_name, compagnies, clients)
    #     ihm.afficher("Sauvegarde effectuée ! À bientôt !")
    # else:
    #     ihm.afficher("Les modifications n'ont pas été enregistrées.\n"
    #                  "À bientôt !")
