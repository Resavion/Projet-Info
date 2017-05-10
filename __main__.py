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
        combinaisons, combi_prix, combi_dist = compagnie.chercher_routes_escales(
            aer_dep, aer_arr, escales_max)
        if combinaisons:
            combinaisons_total.extend(zip(combinaisons, combi_prix, combi_dist))

    combinaisons_avec_horaires = []
    for combi in combinaisons_total:
        combi_ok = True
        for route in combi[0]:
            if len(route.horaires) == 0:
                combi_ok = False
        if combi_ok:
            combinaisons_avec_horaires.append(combi)
    print(len(combinaisons_avec_horaires))

    combi_vols = []
    for combi in combinaisons_avec_horaires:
        routes_vols = []
        combi_ok = True
        for route in combi[0]:
            horaires = route.horaires
            horaires.sort(key=lambda s: s.heure_depart)
            vols_tout = []
            for horaire in route.horaires:
                vols = [x for x in horaire.vols
                        if jour_depart <= x.datetime_depart.date() <= jour_plus1
                        and x.places_restantes_classe(classe) > 0]
                if vols:
                    vols_tout.extend(vols)
            if vols_tout:
                routes_vols.append([route, vols_tout])
            else:
                combi_ok = False
                break
        if combi_ok:
            combi_vols.append(routes_vols)

    vols_ok = []
    for combi in combi_vols:
        route, vols = combi[0]
        if len(combi) == 1:
            vols = [x for x in vols if x.datetime_depart.date() == jour_depart]
            vols_ok.append([[route, vols]])
        else:
            premiere_arrivee = vols[0].datetime_arrivee
            premiere_arrivee += timedelta(minutes=20)
            print(route, premiere_arrivee)
            route2, vols2 = combi[1]
            vols2_jour = [x for x in vols2 if x.datetime_depart > premiere_arrivee
                          and x.datetime_depart.date() == jour_depart]
            if len(vols2_jour) == 0:
                vols2_jour = [x for x in vols2
                              if x.datetime_depart > premiere_arrivee]
            dernier_depart = vols2_jour[-1].datetime_depart
            
            if len(combi) == 2:
                vols_ok.append([[route, vols],[route2, vols2]])
            else:
                premiere_arrivee = vols2[0].datetime_arrivee
                premiere_arrivee += timedelta(minutes=20)
                print(route2, premiere_arrivee)
                route3, vols3 = combi[2]
                print(route3, vols3)
                vols3_jour = [x for x in vols3 if x.datetime_depart > premiere_arrivee
                              and x.datetime_depart.date() == jour_depart]
                if len(vols3_jour) == 0:
                    vols3_jour = [x for x in vols3
                                  if x.datetime_depart > premiere_arrivee]
                if len(combi) == 2:
                    vols_ok.append([[route, vols], [route2, vols2], [route3, vols3]])


    #     print(*combi[0])
    #     route1 = combi[0][0]
    #     route2 = combi[0][1]
    #     horaires1 = route1.horaires
    #     horaires1.sort(key=lambda s: s.heure_depart)
    #     horaires2 = route2.horaires
    #     horaires2.sort(key=lambda s: s.heure_depart)
    #
    #     # Premiere arrivee +20 minutes
    #     premiere_arrivee1 = horaires1[0].heure_arrivee
    #     delta = timedelta(minutes=20)
    #     dt = datetime.combine(date.today(), premiere_arrivee1) + delta
    #     premiere_arrivee1 = dt.time()
    #     # Horaires2 après première arrivée
    #     horaires2 = [x for x in horaires2
    #                  if x.heure_depart > premiere_arrivee1]
    #
    #     dernier_depart2 = horaires2[-1].heure_depart
    #     delta = timedelta(minutes=-20)
    #     dt = datetime.combine(date.today(), dernier_depart2) + delta
    #     dernier_depart2 = dt.time()
    #     horaires1 = [x for x in horaires1
    #                  if x.heure_arrivee < dernier_depart2]
    #
    #     print(horaires1[0])
    #     print(horaires2[0])
    #     print(horaires1[-1])
    #     print(horaires2[-1])
    #     # On ne peut garder que le premier horaire2
    #     # après l'arrivée du premier horaire1
    #     # et que le dernier horaire1 avant le départ du
    #     # dernier horaire2


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
