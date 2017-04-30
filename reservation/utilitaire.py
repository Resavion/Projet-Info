from random import randint
from datetime import (datetime,timedelta)
import ihm.console as ihm
from bdd.acces_bdd import (ouvrir_connexion,
                           fermer_connexion,
                           valider_modifs)
import bdd.requetes as r
from reservation.Aeroport import Aeroport
from reservation.Avion import Avion
from reservation.Billet import Billet
from reservation.Client import Client
from reservation.Compagnie import Compagnie
from reservation.ConfigAvion import ConfigAvion
from reservation.Horaire import Horaire
from reservation.Piste import Piste
from reservation.Reservation import Reservation
from reservation.Route import Route
from reservation.Segment import Segment
from reservation.TypeAvion import TypeAvion
from reservation.Vol import Vol


def charger_bd(db_name):
    """
    Charger en mémoire les informations contenues dans la bdd.

    :param db_name: chemin de la base
    :return: aeroports, compagnies, clients
    """
    conn, cur = ouvrir_connexion(db_name)

    # Aeroports
    aeroports = charger_aeroports(cur)

    # Types d'avions
    types_avions = charger_types_avions(cur)

    # Compagnies
    compagnies = []
    horaires_tout = []
    vols_tout = []
    rows = r.select_all(cur, 'Compagnie')
    for row in rows:
        compagnie = Compagnie(*row)
        # Configs
        configs = charger_configs_de_compagnie(cur, types_avions, compagnie)
        compagnie.configs.extend(configs)
        # Avions
        avions = charger_avions_de_compagnie(cur, aeroports, configs, compagnie)
        compagnie.avions.extend(avions)
        # Routes
        routes = charger_routes_de_compagnie(cur, aeroports, compagnie)
        compagnie.routes.extend(routes)
        # Horaires propres
        for route in routes:
            horaires_propres = charger_horaires_propres_de_route(cur, configs, route)
            route.horaires.extend(horaires_propres)
            horaires_tout.extend(horaires_propres)
        # Vols propres
        for horaire in horaires_propres:
            vols = charger_vols_de_horaire(cur, horaire)
            horaire.vols.extend(vols)
            vols_tout.extend(vols)
        compagnies.append(compagnie)
        # print(compagnie)

    # Horaires en codeshare
    for compagnie in compagnies:
        configs = compagnie.configs
        for route in compagnie.routes:
            horaires_codeshare = charger_horaires_codeshare_de_route(
                cur, configs, horaires_tout, route)
            route.horaires.extend(horaires_codeshare)
            horaires_tout.extend(horaires_codeshare)

    # Clients
    clients = []
    rows = r.select_all(cur, 'Client')
    for row in rows:
        date_naissance = datetime.strptime(row[3],"%d/%m/%Y").date()
        client = Client(*row[0:3], date_naissance)
        # Reservations
        resas = charger_resas_de_client(cur, client)
        client.reservations.extend(resas)
        # Billets
        for resa in resas:
            billets = charger_billets_de_resa(cur, resa)
            resa.billets.append(billets)
            # Segments
            for billet in billets:
                segments = charger_segments_de_billet(cur, vols_tout,
                                                      horaires_tout, billet)
                billet.segments.append(segments)
        clients.append(client)

    return aeroports, compagnies, clients


def charger_aeroports(cur):
    aeroports = []
    rows = r.select_all(cur, 'Aeroport')
    for row in rows:
        aeroport = Aeroport(*row)
        # Pistes
        rows_pistes = r.select_pistes_par_aeroport(cur, aeroport.id_code_iata)
        pistes = []
        for row_piste in rows_pistes:
            piste = Piste(row_piste[0], aeroport, *row_piste[2:])
            pistes.append(piste)
            # print(piste)
        aeroport.pistes.extend(pistes)
        aeroports.append(aeroport)
        # print(aeroport)
    return aeroports


def charger_types_avions(cur):
    types_avions = []
    rows = r.select_all(cur,'TypeAvion')
    for row in rows:
        type_avion = TypeAvion(*row)
        types_avions.append(type_avion)
        # print(type_avion)
    return types_avions


def charger_configs_de_compagnie(cur, types_avions, compagnie):
    configs = []
    rows = r.select_all_par_compagnie(cur,'ConfigAvion', compagnie.id_code_iata)
    for row in rows:
        type_avion = [x for x in types_avions if x.id_nom == row[3]][0]
        config = ConfigAvion(*row[0:2], compagnie, type_avion, *row[4:])
        configs.append(config)
        # print(config)
    return configs


def charger_avions_de_compagnie(cur, aeroports, configs, compagnie):
    avions = []
    rows = r.select_all_par_compagnie(cur,'Avion', compagnie.id_code_iata)
    for row in rows:
        config = [x for x in configs if x.id == row[2]][0]
        aeroport = [x for x in aeroports if x.id_code_iata == row[3]][0]
        date_construc = datetime.strptime(row[4],"%d/%m/%Y").date()
        date_der_rev = datetime.strptime(row[5],"%d/%m/%Y").date()
        avion = Avion(row[0], compagnie, config, aeroport,
                      date_construc, date_der_rev, *row[6:])
        avions.append(avion)
        print(avion)
    return avions


def charger_routes_de_compagnie(cur, aeroports, compagnie):
    routes = []
    rows = r.select_all_par_compagnie(cur,'Route', compagnie.id_code_iata)
    for row in rows:
        id_route = row[0]
        dep = [x for x in aeroports if x.id_code_iata == row[2]][0]
        arr = [x for x in aeroports if x.id_code_iata == row[3]][0]
        route = Route(id_route,compagnie,dep,arr,row[4],row[5])
        routes.append(route)
        # print(route)
    return routes


def charger_horaires_propres_de_route(cur, configs, route):
    horaires = []
    rows = r.select_horaires_propres_par_route(cur, route.id)
    for row in rows:
        # Config
        config = [x for x in configs if x.id == row[9]][0]
        # Heures et duree
        dep = datetime.strptime(row[4], "%H:%M").time()
        arr = datetime.strptime(row[5], "%H:%M").time()
        t = datetime.strptime(row[6], "%H:%M")
        dur = timedelta(hours=t.hour, minutes=t.minute)
        # Horaire
        horaire = Horaire(row[0], route, route.compagnie, row[3],
                          dep, arr, dur, row[7], row[8], config)
        horaires.append(horaire)
        # print(horaire)
    return horaires


def charger_horaires_codeshare_de_route(cur, configs, horaires, route):
    horaires_codeshare = []
    rows = r.select_horaires_codeshare_par_route(cur, route.id)
    for row in rows:
        horaire_operateur = [x for x in horaires if x.id == row[8]][0]
        horaire_codeshare = Horaire(row[0], route, route.compagnie,
                                    *row[3:8], horaire_operateur)
        horaires_codeshare.append(horaire_codeshare)
        # print(horaire_codeshare)
    return horaires_codeshare


def charger_vols_de_horaire(cur, horaire):
    vols = []
    rows = r.select_vols_par_horaire(cur, horaire.id)
    avions = horaire.compagnie.avions
    for row in rows:
        # Avion
        avion = None
        if row[5] is not None:
            avion = [x for x in avions if x.id == row[5]][0]
        # Jours, heures et durees
        dep = datetime.strptime(row[2], "%d/%m/%Y-%H:%M")
        arr = datetime.strptime(row[3], "%d/%m/%Y-%H:%M")
        t = datetime.strptime(row[4], "%H:%M")
        dur = timedelta(hours=t.hour, minutes=t.minute)
        # Vol
        vol = Vol(row[0], horaire, dep, arr, dur, avion, *row[6:])
        vols.append(vol)
        # print(vol)
    return vols


def charger_resas_de_client(cur, client):
    resas = []
    rows = r.select_resas_par_client(cur, client.id)
    for row in rows:
        achat = datetime.strptime(row[3], "%d/%m/%Y-%H:%M:%S")
        resa = Reservation(row[0], client, row[2], achat)
        resas.append(resa)
        # print(resa)
    return resas


def charger_billets_de_resa(cur, resa):
    billets = []
    rows = r.select_billets_par_resa(cur, resa.id)
    for row in rows:
        date_naissance = datetime.strptime(row[6], "%d/%m/%Y").date()
        billet = Billet(row[0], resa, *row[2:6], date_naissance, row[7])
        billets.append(billet)
        # print(billet)
    return billets


def charger_segments_de_billet(cur, vols, horaires, billet):
    segments = []
    rows = r.select_segments_par_billet(cur, billet.id)
    for row in rows:
        vol = [x for x in vols if x.id == row[2]][0]
        horaire = [x for x in horaires if x.id == row[3]][0]
        segment = Segment(row[0], billet, vol, horaire, *row[4:])
        segments.append(segment)
        # print(segment)
    return segments


def update_bd(db_name, compagnies, clients):
    """
    Charger en mémoire les informations contenues dans la bdd.

    :param db_name: chemin de la base
    :param compagnies: compagnies avec leurs routes, horaires, vols et avions
    :param clients: clients avec leurs reservations, billets et segments
    """
    conn, cur = ouvrir_connexion(db_name)

    # Avions
    colonnes = ('id', 'id_compagnie', 'id_config', 'id_aeroport', 'date_construction',
                'date_derniere_revision', 'id_etat', 'position')
    # Pour chaque compagnie
    for compagnie in compagnies:
        for avion in compagnie.avions:
            row = r.select_avion_par_id(cur, avion.id)
            if not row:
                # Insérer avion dans bd
                values = (avion.id, avion.compagnie.id_code_iata,
                          avion.config.id,)
                r.insert_into(cur, 'Avion', colonnes, values)

    # # Un dresseur avec un nom et une liste de pokemon
    # # Les espèces existent déjà, juste nom suffit
    # # Si le pokemon existe, mettre à jour (update), sinon créer (insert)
    # # Si dresseur n'existe pas, créer (insert)
    # conn, cur = ouvrir_connexion(db_name)
    # row = r.select_dresseur_by_nom(cur, joueur.nom)
    # if not row:
    #     # Insérer dresseur dans bd
    #     r.insert_into(cur, 'Dresseur', ('nom', 'type'), (joueur.nom, 1))
    # # pour chaque pokemon
    # for pok in joueur.pokemons:
    #     row = r.select_pokemon_by_nom(cur, pok.nom)
    #     if row:
    #         # Update le pokemon
    #         col = ('pv', 'niveau', 'experience')
    #         values = (pok.pv, pok.niveau, pok.experience)
    #         r.update(cur, 'Pokemon', col, values, pok.nom)
    #     else:
    #         # Insert le pokemon
    #         col = ('nom', 'pv', 'niveau', 'experience', 'espece', 'dresseur')
    #         values = (pok.nom, pok.pv, pok.niveau, pok.experience, pok.espece.nom, joueur.nom)
    #         r.insert_into(cur, 'Pokemon', col, values)
    #         # Insert le lien attaque/pok
    #         for att in pok.attaques:
    #             r.insert_into(cur, 'PokemonAtt', ('nom_pok', 'nom_att'), (pok.nom, att.nom))
    # valider_modifs(conn)
