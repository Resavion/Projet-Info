import os
import numpy as np

import matplotlib.pyplot as plt

import ihm.console as ihm
import utilitaires.earth as earth
from utilitaires.carte import mercator

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
    print('\n')
    client = clients[0]
    #print(clients[0])
    # for reservation in client.reservations:
    #     print(reservation)
    # reservation = client.reservations[0]
    # reservation.fournir_recapitulatif()


    print('\n\n OHAYOOOOOOOOOOOOOOOOOOOO')


    def actions_visualisation(compagnies,aeroports):
        # Proposer les actions
        while True:
            actions = ('Gérer un aéroport',
                       'Afficher la carte de tous les aéroports',
                       'Afficher la carte de toutes les routes')

            action = ihm.choisir(actions, "Choisissez une action :")
            if action == actions[0]:
                choisir_par_code_aeroport(aeroports)
                # aeroports.choisir_par_code_aeroport()
            elif action == actions[1]:
                afficher_carte_aeroports(aeroports)
                # aeroports.afficher_carte_aeroports()
            elif action == action[2]:
                afficher_carte_routes(compagnies)
                # compagnies.afficher_carte_routes()
            else:
                break
        return



    # VERSION SELF ??




    def choisir_par_code_aeroport(aeroports):
        aeroport = None
        code = ihm.demander(
            "Tapez le code IATA (2 caractères) ou ICAO (3 caractères) :")
        results = [x for x in aeroports
                   if x.id_code_iata == code or x.code_icao == code]
        if len(results) == 0:
            ihm.afficher("Désolé, nous n'avons pas trouvé votre aéroport !")
        elif len(results) > 1:
            aeroport = ihm.choisir(results, "Précisez votre choix :")
        else:
            aeroport = results[0]
        if aeroport is not None:
            ihm.afficher("Vous allez gérer l'aéroport {}".format(aeroport))
        return aeroport


    choisir_par_code_aeroport(aeroports)


    def afficher_carte_aeroports(aeroports, show=True):
        """
        Methode qui permet d'afficher la carte des routes de la compagnie
        :return:
        """

        # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        if show:
            # Lecture du trait de cotes
            coords_latlon = np.genfromtxt('utilitaires/coast.txt')
            # Transfo en Mercator
            x, y = mercator(coords_latlon, earth.E, 0, 0, 6378137.0)
            # Ajout a la carte
            plt.fill(x, y, 'bisque', linewidth=0.1)

        # Ajout de la carte de chaque station
        for aeroport in aeroports:
            aeroport.afficher_carte(show=False, annot=False)

        # Affichage
        if show:
            plt.title('Carte de toutes les aéroports')
            plt.show()

    afficher_carte_aeroports(aeroports)



    def afficher_carte_routes(compagnies, show=True):
        """
        Methode qui permet d'afficher la carte des routes de la compagnie
        :return:
        """

        # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        if show:
            # Lecture du trait de cotes
            coords_latlon = np.genfromtxt('utilitaires/coast.txt')
            # Transfo en Mercator
            x, y = mercator(coords_latlon, earth.E, 0, 0, 6378137.0)
            # Ajout a la carte
            plt.fill(x, y, 'bisque', linewidth=0.1)

        # Ajout de la carte de chaque station
        for compagnie in compagnies:
            compagnie.afficher_carte_routes(show=False, annot=False)

        # Affichage
        if show:
            plt.title('Carte de toutes les routes')
            plt.show()


    # afficher_carte_routes(compagnies)

    def nb_routes_sans_double(compagnie):
        """
        Methode qui permet de savoir combien de route sans doublon une compagnie a 
        :param compagnie: 
        :return: 
        """
        nb_routes_double = 0
        for route in compagnie.routes:
            for terou in compagnie.routes:
                if route.aeroport_depart.id_code_iata == terou.aeroport_arrivee.id_code_iata:
                    if route.aeroport_arrivee.id_code_iata == terou.aeroport_depart.id_code_iata:
                        nb_routes_double += 1
        nb_routes_double = nb_routes_double / 2
        nb_routes_sans_double = len(compagnie.routes) - nb_routes_double
        return(nb_routes_sans_double)

    def ranger_liste_aeroport(compagnies):
        liste_a_trier = []
        for compagnie in compagnies:
            nb_route = nb_routes_sans_double(compagnie)
            liste_a_trier.append((compagnie, nb_route))
        nb_aeroport = len(liste_a_trier)
        if nb_aeroport <= 1:
            print(liste_a_trier)
        for i in range(nb_aeroport):
            for j in range(nb_aeroport):
                if liste_a_trier[i][1] >= liste_a_trier[j][1]:
                    stock = liste_a_trier[i]
                    liste_a_trier[i] = liste_a_trier[j]
                    liste_a_trier[j] = stock

        return(liste_a_trier)

    # liste_a_trier = ranger_liste_aeroport(compagnies)

    # ihm.afficher_paginer(liste_a_trier, 'BLABLABLA')



    # a = nb_routes_sans_double(compagnies[0])
    # print(a)
    # b = nb_routes_sans_double(compagnies[1])
    # print(b)
    # c = nb_routes_sans_double(compagnies[2])
    # print(c)
    # d = nb_routes_sans_double(compagnies[3])
    # print(d)
    #
    # l= [a,b,c,d]
    # for i in range(len(l)):
    #     for j in range(len(l)):
    #         if l[i]>=l[j]:
    #             z = l[i]
    #             l[i] = l[j]
    #             l[j] = z
    # print(l)
    # liste_routes_sans_double = NH.routes
    # for route in NH.routes:
    #     for new in liste_routes_sans_double:
    #         if route.aeroport_depart.id_code_iata == new.aeroport_arrivee.id_code_iata and\
    #             route.aeroport_arrivee.id_code_iata == new.aeroport_depart.id_code_iata:
    #                 liste_routes_sans_double -= new
    # print(liste_routes_sans_double)



    # for compagnie in compagnies:
    #     print(compagnie._id_code_iata)
    #     for route in compagnie.routes:
    #         # print(route.id)
    #         print(route.aeroport_depart.id_code_iata)
    #         print(route.aeroport_arrivee.id_code_iata)

    def afficher_aeroports():
        pass

    # while True:
    #     # Choisir un mode d'utilisation
    #     modes = ('Client', 'Compagnie', 'Visualisation seule', 'Quitter')
    #     choix = ihm.choisir(modes, "Choisissez un mode d'utilisation :")
    #
    #     # Si Client
    #     if choix == modes[0]:
    #         menus.actions_client(clients, compagnies, aeroports)
    #     # Si Compagnie
    #     elif choix == modes[1]:
    #         menus.actions_compagnie(compagnies)
    #     # Si Visualisation
    #     elif choix == modes[2]:
    #         pass
    #     # Sinon on veut quitter le programme
    #     else:
    #         break
    #
    # ihm.afficher("Vous quittez le programme.")
    # liste_choix = ('Oui', 'Non')
    # choix = ihm.choisir(liste_choix,
    #                     "Voulez-vous sauvegarder vos modifications ?")
    # if choix == 'Oui':
    #     update_bd(db_name, compagnies, clients)
    #     ihm.afficher("Sauvegarde effectuée ! À bientôt !")
    # else:
    #     ihm.afficher("Les modifications n'ont pas été enregistrées.\n"
    #                  "À bientôt !")
