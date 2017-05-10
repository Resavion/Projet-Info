import os
from datetime import date, datetime, timedelta

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
    aer_arr = Aeroport.find_by_id("OKA")
    escales_max = 2
    classe = 'C'
    jour_depart = date(2017,5,11)
    jour_plus1 = jour_depart.replace(day=jour_depart.day+1)

    combinaisons_total = []
    for compagnie in compagnies:
        combinaisons = compagnie.chercher_routes_escales(
            aer_dep, aer_arr, escales_max)
        if combinaisons:
            combinaisons_total.extend(combinaisons)

    # On garde les combinaisons avec horaires en base
    combinaisons_avec_horaires = []
    for combi in combinaisons_total:
        combi_ok = True
        for route in combi:
            if len(route.horaires) == 0:
                combi_ok = False
        if combi_ok:
            combinaisons_avec_horaires.append(combi)

    # On recupere les vols pour chaque combinaison
    combi_vols = []
    for combi in combinaisons_avec_horaires:
        routes_vols = []
        combi_ok = True
        # Pour chaque route de la combinaison
        for route in combi:
            vols_tout = route.chercher_vols(jour_depart, classe)
            # Si on a trouve des vols pour la route, on enregistre
            if vols_tout:
                routes_vols.append([route, vols_tout])
            # Sinon la route n'est pas disponible
            else:
                combi_ok = False
                break
        if combi_ok:
            combi_vols.append(routes_vols)

    vols_ok = []
    for combi in combi_vols:
        route, vols = combi[0]
        # Si le trajet n'a pas d'escale, on enregistre tous les vols du jour
        if len(combi) == 1:
            vols = [x for x in vols if x.datetime_depart.date() == jour_depart]
            vols_ok.append([[route, vols]])
        # Sinon
        else:
            # On regarde la premiere arrivee + 20 minutes
            premiere_arrivee = vols[0].datetime_arrivee
            premiere_arrivee += timedelta(minutes=20)
            route2, vols2 = combi[1]
            # Parmi les vols en correspondance, on enleve ceux avant la premiere arrivee
            # On prend les vols du jour demande de preference
            vols2_jour = [x for x in vols2 if x.datetime_depart > premiere_arrivee
                          and x.datetime_depart.date() == jour_depart]
            # Sinon on prend le jour d'apres
            if len(vols2_jour) == 0:
                vols2_jour = [x for x in vols2
                              if x.datetime_depart > premiere_arrivee]
            vols2 = vols2_jour
            # On regarde le dernier depart de correspondance - 20 minutes
            dernier_depart = vols2[-1].datetime_depart
            dernier_depart -= timedelta(minutes=20)
            # On enleve les vols qui arrivent apres le dernier depart
            vols = [x for x in vols if x.datetime_arrivee < dernier_depart]
            # Si le trajet ne comporte qu'une seule escale, on enregistre
            if len(combi) == 2:
                vols_ok.append([[route, vols],[route2, vols2]])
            # Sinon
            else:
                # Meme chose
                premiere_arrivee = vols2[0].datetime_arrivee
                premiere_arrivee += timedelta(minutes=20)
                route3, vols3 = combi[2]
                # On garde ceux qui partent apres la premiere arrivee
                vols3_jour = [x for x in vols3 if x.datetime_depart > premiere_arrivee
                              and x.datetime_depart.date() == jour_depart]
                if len(vols3_jour) == 0:
                    vols3_jour = [x for x in vols3
                                  if x.datetime_depart > premiere_arrivee]
                vols3 = vols3_jour
                # On garde ceux qui arrivent avant le dernier depart
                dernier_depart = vols3[-1].datetime_depart
                dernier_depart -= timedelta(minutes=20)
                vols2 = [x for x in vols2 if x.datetime_arrivee < dernier_depart]
                dernier_depart = vols2[-1].datetime_depart
                dernier_depart -= timedelta(minutes=20)
                vols = [x for x in vols if x.datetime_arrivee < dernier_depart]
                # On enregistre
                vols_ok.append([[route, vols], [route2, vols2_jour], [route3, vols3]])

    for combi in vols_ok:
        for route, vols in combi:
            print(route, *vols)

    #
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
