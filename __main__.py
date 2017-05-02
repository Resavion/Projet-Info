import os
import operator
from datetime import datetime

import ihm.console as ihm
from bdd.config_bdd import (creer_bdd, inserer_jeu_test)
from reservation.utilitaire import (charger_bd, update_bd)
from reservation.Client import Client
from reservation.Compagnie import Compagnie


if __name__ == '__main__':
    db_name = "bdd/resavion.db"
    if not os.path.exists(db_name):
        creer_bdd(db_name)
        inserer_jeu_test(db_name)

    aeroports, compagnies, clients = charger_bd(db_name)

    # Choisir un mode d'utilisation
    modes = ('Client', 'Gestionnaire de compagnie')
    choix = ihm.choisir(modes, "Choisissez un mode d'utilisation :")

    # Si Client : choisir si existant ou nouveau
    if choix == 'Client':
        comptes = [client for client in clients]
        comptes.append('Nouveau client')
        client = ihm.choisir(
            comptes, "Choisissez un client sauvegardé ou "
                     "créez un nouveau client")

        # Si nouveau : demander infos
        if client == 'Nouveau client':
            new_id = clients[-1].id + 1
            nom = ihm.demander("Saisissez votre nom :")
            prenom = ihm.demander("Saisissez votre prénom :")
            while True:
                try:
                    date_naiss = ihm.demander(
                        "Saisissez votre date de naissance (AAAA-MM-JJ) :")
                    date_naiss = datetime.strptime(date_naiss, '%Y-%m-%d')
                except ValueError:
                    ihm.afficher("Ceci n'est pas une date valide.")
                    pass
                else:
                    date_naiss = date_naiss.date()
                    break
            client = Client(new_id, nom, prenom, date_naiss)
            clients.append(client)

        # Le client est chargé
        ihm.afficher("Bonjour {} !".format(client.prenom))

        # Demander action : Faire, Consulter, Modifier, Se déconnecter
        actions = ('Faire une réservation', 'Consulter ses réservations',
                   'Modifier une réservation', 'Annuler une réservation')
        action = ihm.choisir(actions, "Choisissez une action :")
        if action == actions[0]:
            client.faire_reservation()
        elif action == actions[1]:
            client.consulter_reservations()
        elif action == actions[2]:
            client.modifier_reservation()
        else:
            client.annuler_reservation()
    # Sinon : c'est un gestionnaire de compagnie
    else:
        # On demande de choisir une compagnie
        actions = ('Recherche par continent','Recherche par code IATA ou ICAO')
        recherche = ihm.choisir(actions, "Choisissez un mode de recherche :")
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
                if borne_bas > 0:
                    liste.append("Voir les compagnies précédentes")
                if borne_haut < len(compagnies_filtre):
                    liste.append("Voir les compagnies suivantes")
                compagnie = ihm.choisir(liste, "Choisissez une compagnie :")
                if compagnie == "Voir les compagnies suivantes":
                    borne_bas = borne_haut
                elif compagnie == "Voir les compagnies précédentes":
                    borne_haut = borne_bas
                    borne_bas -= pas
                else:
                    break
            print(compagnie)

    # Demander action :

    # update_bd(db_name, compagnies, clients)
