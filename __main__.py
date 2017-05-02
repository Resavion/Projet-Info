import os

import ihm.console as ihm
from bdd.config_bdd import (creer_bdd, inserer_jeu_test)
from utilitaires.chargement import (charger_bd,
                                    update_bd)
from utilitaires.menus import (ajouter_client)


if __name__ == '__main__':
    db_name = "bdd/resavion.db"
    if not os.path.exists(db_name):
        creer_bdd(db_name)
        inserer_jeu_test(db_name)

    aeroports, compagnies, clients = charger_bd(db_name)

    while True:
        # Choisir un mode d'utilisation
        modes = ('Client', 'Gestionnaire de compagnie', 'Quitter')
        choix = ihm.choisir(modes, "Choisissez un mode d'utilisation :")

        # Si Client
        if choix == modes[0]:
            # Choisir un client existant ou nouveau
            comptes = [client for client in clients]
            comptes.append('Nouveau client')
            client = ihm.choisir(
                comptes, "Choisissez un client sauvegardé ou "
                         "créez un nouveau client")

            # Si nouveau : demander infos et créer client
            if client == 'Nouveau client':
                client = ajouter_client(clients)
                clients.append(client)

            # Le client est chargé
            ihm.afficher("Bonjour {} !".format(client.prenom))

            # Demander action : Faire, Consulter, Modifier, Annuler
            actions = ('Faire une réservation', 'Consulter ses réservations',
                       'Modifier une réservation', 'Annuler une réservation',
                       'Revenir au début')
            action = ihm.choisir(actions, "Choisissez une action :")
            if action == actions[0]:
                client.faire_reservation()
            elif action == actions[1]:
                client.consulter_reservations()
            elif action == actions[2]:
                client.modifier_reservation()
            elif action == actions[3]:
                client.annuler_reservation()
            else:
                pass

        # Sinon : c'est un gestionnaire de compagnie
        elif choix == modes[1]:
            # On demande de choisir une compagnie
            actions = ('Recherche par continent',
                       'Recherche par code IATA ou ICAO',
                       'Revenir au début')
            recherche = ihm.choisir(actions, "Choisissez un mode de recherche :")

            # Si recherche par continents
            if recherche == actions[0]:
                continents = {'Amérique du Nord':'NA', 'Amérique du Sud':'SA',
                              'Europe':'EU', 'Afrique':'AF', 'Asie':'AS',
                              'Océanie':'OC'}
                nom = ihm.choisir([*continents.keys()],
                                  "Choisissez un continent :")
                compagnies.sort(key=lambda s: len(s.routes),reverse=True)
                compagnies_filtre = [x for x in compagnies
                                     if x.code_continent == continents[nom]]
                borne_bas = 0
                pas = 2
                compagnie = None
                while True:
                    borne_haut = min(len(compagnies_filtre), borne_bas+pas)
                    liste = compagnies_filtre[borne_bas:borne_haut]
                    if len(liste) == 0:
                        ihm.afficher("Il n'y a pas de compagnie disponible !")
                        break
                    if borne_bas > 0:
                        liste.append("Voir les compagnies précédentes")
                    if borne_haut < len(compagnies_filtre):
                        liste.append("Voir les compagnies suivantes")
                    # Faire le choix
                    compagnie = ihm.choisir(liste, "Choisissez une compagnie :")
                    if compagnie == "Voir les compagnies suivantes":
                        borne_bas = borne_haut
                    elif compagnie == "Voir les compagnies précédentes":
                        borne_haut = borne_bas
                        borne_bas -= pas
                    else:
                        print(compagnie)
                        break
            # Si recherche par code
            elif recherche == actions[1]:
                test = True
            # Sinon on revient au début
            else:
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
