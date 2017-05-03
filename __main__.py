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

    while True:
        # Choisir un mode d'utilisation
        modes = ('Client', 'Compagnie', 'Visualisation seule', 'Quitter')
        choix = ihm.choisir(modes, "Choisissez un mode d'utilisation :")

        # Si Client
        if choix == modes[0]:
            menus.actions_client(clients, compagnies, aeroports)
        # Si Compagnie
        elif choix == modes[1]:
            menus.actions_compagnie(compagnies)
        # Si Visualisation
        elif choix == modes[2]:
            pass
        # Sinon on veut quitter le programme
        else:
            break

    ihm.afficher("Vous quittez le programme.")
    liste_choix = ('Oui', 'Non')
    choix = ihm.choisir(liste_choix,
                        "Voulez-vous sauvegarder vos modifications ?")
    if choix == 'Oui':
        update_bd(db_name, compagnies, clients)
        ihm.afficher("Sauvegarde effectuée ! À bientôt !")
    else:
        ihm.afficher("Les modifications n'ont pas été enregistrées.\n"
                     "À bientôt !")
