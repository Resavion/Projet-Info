from datetime import (datetime, timedelta)
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
    compagnies, horaires_tout, vols_tout = \
        charger_compagnies(cur, aeroports, types_avions)

    # Clients
    clients = charger_clients(cur, horaires_tout, vols_tout)

    fermer_connexion(cur, conn)
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


def charger_compagnies(cur, aeroports, types_avions):
    compagnies = []
    horaires_tout = []
    vols_tout = []
    # Compagnies
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
        for route in compagnie.routes:
            horaires_codeshare = charger_horaires_codeshare_de_route(
                cur, horaires_tout, route)
            route.horaires.extend(horaires_codeshare)
            horaires_tout.extend(horaires_codeshare)
    return compagnies, horaires_tout, vols_tout


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
        date_construc = datetime.strptime(row[4],"%Y-%m-%d").date()
        date_der_rev = datetime.strptime(row[5],"%Y-%m-%d").date()
        avion = Avion(row[0], compagnie, config, aeroport,
                      date_construc, date_der_rev, *row[6:])
        avions.append(avion)
        aeroport.avions.append(avion)
        # print(avion)
    return avions


def charger_routes_de_compagnie(cur, aeroports, compagnie):
    routes = []
    rows = r.select_all_par_compagnie(cur,'Route', compagnie.id_code_iata)
    for row in rows:
        id_route = row[0]
        dep = [x for x in aeroports if x.id_code_iata == row[2]][0]
        arr = [x for x in aeroports if x.id_code_iata == row[3]][0]
        route = Route(id_route, compagnie, dep, arr, row[4], row[5])
        routes.append(route)
        dep.routes_sortantes.append(route)
        arr.routes_entrantes.append(route)
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
        t = datetime.strptime(row[6], "%Hh%M")
        dur = timedelta(hours=t.hour, minutes=t.minute)
        # Horaire
        horaire = Horaire(row[0], route, route.compagnie, row[3],
                          dep, arr, dur, row[7], row[8], config)
        horaires.append(horaire)
        # print(horaire)
    return horaires


def charger_horaires_codeshare_de_route(cur, horaires, route):
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
        dep = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        arr = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
        t = datetime.strptime(row[4], "%H:%M:%S")
        dur = timedelta(hours=t.hour, minutes=t.minute)
        # Vol
        vol = Vol(row[0], horaire, dep, arr, dur, avion, *row[6:])
        vols.append(vol)
        if avion is not None:
            avion.vols.append(vol)
        # print(vol)
    return vols


def charger_clients(cur, horaires, vols):
    clients = []
    rows = r.select_all(cur, 'Client')
    for row in rows:
        date_naissance = datetime.strptime(row[3],"%Y-%m-%d").date()
        client = Client(*row[0:3], date_naissance)
        # Reservations
        resas = charger_resas_de_client(cur, client)
        client.reservations.extend(resas)
        # Billets
        for resa in resas:
            billets = charger_billets_de_resa(cur, resa)
            resa.billets.extend(billets)
            # Segments
            for billet in billets:
                segments = charger_segments_de_billet(cur, horaires, vols, billet)
                billet.segments.extend(segments)
        clients.append(client)
    return clients


def charger_resas_de_client(cur, client):
    resas = []
    rows = r.select_resas_par_client(cur, client.id)
    for row in rows:
        achat = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
        resa = Reservation(row[0], client, row[2], achat)
        resas.append(resa)
        # print(resa)
    return resas


def charger_billets_de_resa(cur, resa):
    billets = []
    rows = r.select_billets_par_resa(cur, resa.id)
    for row in rows:
        date_naissance = datetime.strptime(row[6], "%Y-%m-%d").date()
        billet = Billet(row[0], resa, *row[2:6], date_naissance, row[7])
        billets.append(billet)
        # print(billet)
    return billets


def charger_segments_de_billet(cur, horaires, vols, billet):
    segments = []
    rows = r.select_segments_par_billet(cur, billet.id)
    for row in rows:
        vol = [x for x in vols if x.id == row[2]][0]
        horaire = [x for x in horaires if x.id == row[3]][0]
        segment = Segment(row[0], billet, vol, horaire, *row[4:])
        segments.append(segment)
        vol.segments.append(segment)
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
    # Pour chaque compagnie
    for compagnie in compagnies:
        for avion in compagnie.avions:
            update_avion(cur, avion)
    valider_modifs(conn)

    # Vols
    # Pour chaque compagnie
    for compagnie in compagnies:
        for route in compagnie.routes:
            for horaire in route.horaires:
                for vol in horaire.vols:
                    update_vol(cur, vol)
    valider_modifs(conn)

    # Clients
    for client in clients:
        row = r.select_par_id(cur, 'Client', client.id)
        if not row:
            # Insérer client dans bd
            colonnes = ('id','nom','prenom','date_naissance')
            values = (client.id, client.nom, client.prenom, client.date_naissance)
            r.insert_into(cur, 'Client', colonnes, values)
            print("insert {}".format(client))
    valider_modifs(conn)

    # Reservations
    # Pour chaque client
    for client in clients:
        for resa in client.reservations:
            row = r.select_par_id(cur, 'Reservation', resa.id)
            if not row:
                # Insérer resa dans bd
                colonnes = ('id','id_client','prix_total','date_achat')
                values = (resa.id, resa.client.id, resa.prix_total, resa.date_achat)
                r.insert_into(cur, 'Reservation', colonnes, values)
                print("insert {}".format(resa))
    valider_modifs(conn)

    # Billets
    # Pour chaque client
    for client in clients:
        for resa in client.reservations:
            for billet in resa.billets:
                update_billet(cur, billet)
    valider_modifs(conn)

    # Segments
    # Pour chaque client
    for client in clients:
        for resa in client.reservations:
            for billet in resa.billets:
                for segment in billet.segments:
                    update_segment(cur, segment)
    valider_modifs(conn)

    fermer_connexion(cur, conn)


def update_avion(cur, avion):
    row = r.select_par_id(cur, 'Avion', avion.id)
    if not row:
        # Insérer avion dans bd
        colonnes = ('id', 'id_compagnie', 'id_config', 'id_aeroport',
                    'date_construction', 'date_derniere_revision',
                    'id_etat', 'position')
        values = (avion.id, avion.compagnie.id_code_iata,
                  avion.config.id, avion.aeroport.id_code_iata,
                  avion.date_construction, avion.date_derniere_revision,
                  avion.etat, avion.position)
        r.insert_into(cur, 'Avion', colonnes, values)
        print("insert {}".format(avion))
    else:
        # Update avion dans bd
        colonnes = ('id_config', 'id_aeroport', 'date_derniere_revision',
                    'id_etat', 'position')
        values = (avion.config.id, avion.aeroport.id_code_iata,
                  avion.date_derniere_revision, avion.etat, avion.position)
        r.update(cur, 'Avion', colonnes, values, avion.id)
        print("update {}".format(avion))


def update_vol(cur, vol):
    row = r.select_par_id(cur, 'Vol', vol.id)
    if not row:
        # Insérer vol dans bd
        colonnes = ('id', 'id_horaire', 'datetime_depart',
                    'datetime_arrivee', 'duree', 'id_avion',
                    'places_restantes_premiere', 'places_restantes_business',
                    'places_restantes_eco_plus', 'places_restantes_eco',
                    'statut', 'cabine')
        values = (vol.id, vol.horaire.id,
                  vol.datetime_depart, vol.datetime_arrivee,
                  "{}".format(vol.duree), vol.avion.id,
                  vol.places_restantes_premiere, vol.places_restantes_business,
                  vol.places_restantes_eco_plus, vol.places_restantes_eco,
                  vol.statut, vol.cabine)
        r.insert_into(cur, 'Vol', colonnes, values)
        print("insert {}".format(vol))
    else:
        # Update vol dans bd
        colonnes = ('datetime_depart', 'datetime_arrivee',
                    'duree', 'id_avion', 'places_restantes_premiere',
                    'places_restantes_business', 'places_restantes_eco_plus',
                    'places_restantes_eco', 'statut', 'cabine')
        values = (vol.datetime_depart, vol.datetime_arrivee,
                  "{}".format(vol.duree), vol.avion.id,
                  vol.places_restantes_premiere, vol.places_restantes_business,
                  vol.places_restantes_eco_plus, vol.places_restantes_eco,
                  vol.statut, vol.cabine)
        r.update(cur, 'Vol', colonnes, values, vol.id)
        print("update {}".format(vol))


def update_billet(cur, billet):
    row = r.select_par_id(cur, 'Billet', billet.id)
    if not row:
        # Insérer billet dans bd
        colonnes = ('id', 'id_reservation', 'tarif',
                    'nom_passager', 'prenom_passager', 'passeport',
                    'date_naissance', 'options')
        values = (billet.id, billet.reservation.id, billet.tarif,
                  billet.nom_passager, billet.prenom_passager,
                  billet.passeport, billet.date_naissance,
                  billet.options)
        r.insert_into(cur, 'Billet', colonnes, values)
        print("insert {}".format(billet))
    else:
        # Update billet dans bd
        colonnes = ('tarif', 'nom_passager', 'prenom_passager',
                    'passeport', 'date_naissance', 'options')
        values = (billet.tarif, billet.nom_passager,
                  billet.prenom_passager, billet.passeport,
                  billet.date_naissance, billet.options)
        r.update(cur, 'Billet', colonnes, values, billet.id)
        print("update {}".format(billet))


def update_segment(cur, segment):
    row = r.select_par_id(cur, 'Segment', segment.id)
    if not row:
        # Insérer segment dans bd
        colonnes = ('id_billet','id_vol','id_horaire','place','option')
        values = (segment.billet.id, segment.vol.id, segment.horaire.id,
                  segment.place, segment.options)
        r.insert_into(cur, 'Segment', colonnes, values)
        print("insert {}".format(segment))
    else:
        # Update segment dans bd
        colonnes = ('id_vol','id_horaire','place','option')
        values = (segment.vol.id, segment.horaire.id,
                  segment.place, segment.options)
        r.update(cur, 'Segment', colonnes, values, segment.id)
        print("update {}".format(segment))

