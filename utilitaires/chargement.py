from datetime import (datetime, timedelta)
from pytz import timezone

from bdd.acces_bdd import (ouvrir_connexion,
                           fermer_connexion,
                           valider_modifs)
import bdd.requetes as r
from reservation.Enums import (EnumAvion, EnumOption, EnumStatutVol)
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

    conn, cur    = ouvrir_connexion(db_name)

    # Aeroports
    aeroports    = charger_aeroports(cur)

    # Types d'avions
    types_avions = charger_types_avions(cur)

    # Compagnies
    compagnies, horaires_tout, vols_tout = \
        charger_compagnies(cur, types_avions)

    # Clients
    clients = charger_clients(cur, horaires_tout, vols_tout)

    fermer_connexion(cur, conn)
    return aeroports, compagnies, clients


def charger_aeroports(cur):
    """
    Methode qui permet de charger les aéroports de la base de données
    
    :param cur: curseur
    :return: la liste des aeroports
    """

    print("Chargement des aeroports...")
    aeroports = []
    rows      = r.select_all(cur, 'Aeroport')
    for row in rows:
        aeroport    = Aeroport(*row[:-1], timezone(row[-1]))
        # Pistes
        rows_pistes = r.select_pistes_par_aeroport(cur, aeroport.id_code_iata)
        pistes      = []
        for row_piste in rows_pistes:
            piste = Piste(row_piste[0], aeroport, *row_piste[2:])
            pistes.append(piste)
            # print(piste)
        aeroport.pistes.extend(pistes)
        aeroports.append(aeroport)
        # print(aeroport)
    return aeroports


def charger_types_avions(cur):
    """
    Methode qui permet de charger les types d'avion de la base de données
    
    :param cur: curseur
    :return: la liste des types d'avion
    """

    types_avions = []
    rows         = r.select_all(cur,'TypeAvion')
    for row in rows:
        type_avion = TypeAvion(*row)
        types_avions.append(type_avion)
        # print(type_avion)
    return types_avions


def charger_compagnies(cur, types_avions):
    """
    Methode qui permet de charger les differentes compagnies avec leurs différents horaires et vols
    
    :param cur: curseur
    :param types_avions: tous les types d'avion de la base de données
    :return: toutes les compagnies avec leurs horaires et leurs vols
    """

    print("Chargement des compagnies...")
    compagnies    = []
    horaires_tout = []
    vols_tout     = []
    # Compagnies
    rows          = r.select_all(cur, 'Compagnie')
    for row in rows:
        compagnie = Compagnie(*row)
        # Configs
        configs   = charger_configs_de_compagnie(cur, types_avions, compagnie)
        compagnie.configs.extend(configs)
        # Avions
        avions    = charger_avions_de_compagnie(cur, configs, compagnie)
        compagnie.avions.extend(avions)
        # Routes
        routes    = charger_routes_de_compagnie(cur, compagnie)
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
    """
    Methode qui permet de charger liste des configurations des avions proposees par la compagnie
    :param cur: curseur
    :param types_avions: la liste des types d'avions
    :param compagnie: l'objet compagnie
    :return: la liste des configurations des avions proposees par la compagnie
    """

    configs = []
    rows    = r.select_all_par_compagnie(cur,'ConfigAvion', compagnie.id_code_iata)
    for row in rows:
        type_avion  = [x for x in types_avions if x.id == row[2]][0]
        disposition = row[8]
        if not disposition:
            with open('bdd/data/{}_{}.txt'.format(*row[0:2]), 'r') as myfile:
                disposition = myfile.read()
        config = ConfigAvion(compagnie, row[1], type_avion,
                             *row[3:-1], disposition)
        configs.append(config)
        # print(config)
    return configs


def charger_avions_de_compagnie(cur, configs, compagnie):
    """
    Methode qui permet de chargr les avions de la compagnie 
    
    :param cur: curseur
    :param configs: la liste des configurations des avions proposees par la compagnie
    :param compagnie: l'objet compagnie
    :return: la liste des avions de la compagnie
    """

    avions = []
    rows   = r.select_all_par_compagnie(cur,'Avion', compagnie.id_code_iata)
    for row in rows:
        config         = [x for x in configs if x.nom == row[2]][0]
        aeroport = None
        if row[3] != '':
            aeroport   = Aeroport.find_by_id(row[3])
        date_livraison = datetime.strptime(row[4],"%Y-%m-%d").date()
        date_der_rev   = datetime.strptime(row[5],"%Y-%m-%d").date()
        etat           = EnumAvion(row[6])
        avion          = Avion(row[0], compagnie, config, aeroport,
                               date_livraison, date_der_rev, etat, *row[7:])
        avions.append(avion)
        if aeroport is not None:
            aeroport.avions.append(avion)
        # print(avion)
    return avions


def charger_routes_de_compagnie(cur, compagnie):
    """
    Methode qui permet de charger toutes les routes que la compagnie effectue
    
    :param cur: curseur
    :param compagnie: l'objet compagnie
    :return: la liste des routes qu'une compagnie effectue
    """

    print("Chargement des routes de {}...".format(compagnie))
    routes = []
    rows   = r.select_all_par_compagnie(cur,'Route', compagnie.id_code_iata)
    for row in rows:
        dep      = Aeroport.find_by_id(row[1])
        arr      = Aeroport.find_by_id(row[2])
        # row[4] = geom : linestring entre les deux aeroports en WKT
        # row[5] = codeshare : booleen qui permet de savoir si un avion est partage par plusieurs compagnies
        route    = Route(compagnie, dep, arr, row[3], row[4])
        routes.append(route)
        dep.routes_sortantes.append(route)
        arr.routes_entrantes.append(route)
        # print(route)
    return routes


def charger_horaires_propres_de_route(cur, configs, route):
    """
    Methode qui permet de charger l'horaire propre 
    (c'est-à-dire un horaire assuré en propre par la compagnie)
    d'une route par rapport à une compagnie
    
    :param cur: curseur
    :param configs: la liste des configurations des avions proposees par la compagnie
    :param route: la route dont les horaires doivent être chargés
    :return: la liste des horaires propres pour la route
    """

    horaires = []
    rows     = r.select_horaires_propres_par_route(cur, route)
    for row in rows:
        # Config
        config  = [x for x in configs if x.nom == row[5]][0]
        # Heures et duree
        dep     = datetime.strptime(row[6], "%H:%M").time()
        arr     = datetime.strptime(row[7], "%H:%M").time()
        t       = datetime.strptime(row[8], "%Hh%M")
        dur     = timedelta(hours=t.hour, minutes=t.minute)
        # Horaire
        horaire = Horaire(route, row[1], dep, arr, dur, row[9], None, config)
        horaires.append(horaire)
        # print(horaire)
    return horaires


def charger_horaires_codeshare_de_route(cur, horaires, route):
    """
    Methode qui permet de charger les horaires partagés d'une route 
    (c'est-à-dire un horaire qui n'est pas assuré en propre par la compagnie)
    
    :param cur: curseur
    :param horaires: la liste des horaires propres de toutes les compagnies
    :param route: la route dont les horaires doivent être chargés
    :return: la liste des horaires partagés
    """

    horaires_codeshare = []
    rows               = r.select_horaires_codeshare_par_route(cur, route)
    for row in rows:
        horaire_operateur = [x for x in horaires
                             if x.compagnie.id_code_iata == row[10]
                             and x.numero == row[11]][0]
        horaire_codeshare = Horaire(route, row[1], *row[6:10], horaire_operateur)
        horaires_codeshare.append(horaire_codeshare)
        horaire_operateur.horaires_codeshare.append(horaire_codeshare)
        # print(horaire_codeshare)
    return horaires_codeshare


def charger_vols_de_horaire(cur, horaire):
    """
    Methode qui permet de charger tous les vols correspondant a un certain horaire
    
    :param cur: curseur
    :param horaire: l'objet horaire en question
    :return: la liste des vols effectues a l'horaire demande
    """

    vols = []
    rows = r.select_vols_par_horaire(cur, horaire)
    avions = horaire.compagnie.avions
    for row in rows:
        # Avion
        avion = None
        if row[5]:
            avion = [x for x in avions if x.id == row[5]][0]
        # Jours, heures et durees
        dep = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        arr = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
        t   = datetime.strptime(row[4], "%H:%M:%S")
        dur = timedelta(hours=t.hour, minutes=t.minute)
        # Statut
        statut = EnumStatutVol(row[10])
        # Vol
        vol = Vol(horaire, dep, arr, dur, avion, *row[6:10], statut)
        vols.append(vol)
        if avion is not None:
            avion.vols.append(vol)
        # print(vol)
    return vols


def charger_clients(cur, horaires, vols):
    """
    Methode qui permet de charger tous les clients 
    
    :param cur: curseur
    :param horaires: la liste de tous les horaires peut importe la compagnie
    :param vols: la liste de tous les vols
    :return: la liste de tous les clients
    """

    clients = []
    rows    = r.select_all(cur, 'Client')
    for row in rows:
        date_naissance = datetime.strptime(row[3],"%Y-%m-%d").date()
        client         = Client(*row[0:3], date_naissance)
        # Reservations
        resas          = charger_resas_de_client(cur, client)
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
    """
    Methode qui permet de charger toutes les reservations d'un client
    
    :param cur: curseur
    :param client: le client dont on veut charger les reservations
    :return: la liste des reservations
    """

    resas = []
    rows  = r.select_resas_par_client(cur, client.id)
    for row in rows:
        achat = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
        resa  = Reservation(row[0], client, row[2], achat)
        resas.append(resa)
        # print(resa)
    return resas


def charger_billets_de_resa(cur, resa):
    """
    Methode qui permet de charger les billets pour une reservation donnée
    
    :param cur: curseur 
    :param resa: l'objet reservation
    :return: la liste des billets de la reservation
    """

    billets = []
    rows    = r.select_billets_par_resa(cur, resa.id)
    for row in rows:
        date_naissance = datetime.strptime(row[6], "%Y-%m-%d").date()
        options_ids    = r.select_options_par_billet(cur, row[0])
        # on cree une liste d'option
        options        = [EnumOption(*x) for x in options_ids]
        billet         = Billet(row[0], resa, *row[2:6], date_naissance, options)
        billets.append(billet)
        # print(billet)
    return billets


def charger_segments_de_billet(cur, horaires, vols, billet):
    """
    Methode qui permet de charger les segments d'un billet d'avion
    
    :param cur: curseur 
    :param horaires: la listes de tous les horaires
    :param vols: la liste de tous les vols
    :param billet: l'objet billet
    :return: la liste des segments
    """

    segments = []
    rows     = r.select_segments_par_billet(cur, billet.id)
    for row in rows:
        cle_vol = "{}{}{}".format(*row[2:5])
        vol         = Vol.cle_index[cle_vol]
        horaire = vol.horaire
        if row[5]:
            horaire     = [x for x in horaires
                           if x.compagnie.id_code_iata == row[5]
                           and x.numero == row[6]][0]
        options_ids = r.select_options_par_segment(cur, row[0])
        # on cree une liste d'option
        options     = [EnumOption(*x) for x in options_ids]
        segment     = Segment(row[0], billet, vol, horaire, row[7], options)
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
            values   = (client.id, client.nom, client.prenom, client.date_naissance)
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
                values   = (resa.id, resa.client.id, resa.prix_total, resa.date_achat)
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
    """
    Methode qui permet de mettre a jour les informations liées a l'avion
    
    :param cur: curseur 
    :param avion: l'objet avion 
    :return: None
    """

    row = r.select_par_id(cur, 'Avion', avion.id)
    if not row:
        # Insérer avion dans bd
        colonnes = ('id', 'id_compagnie', 'nom_config', 'id_aeroport',
                    'date_livraison', 'date_derniere_revision',
                    'id_etat', 'latitude_deg', 'longitude_deg')
        values   = (avion.id, avion.compagnie.id_code_iata,
                    avion.config.nom, avion.aeroport.id_code_iata,
                    avion.date_livraison, avion.date_derniere_revision,
                    avion.etat.value, avion.latitude_deg, avion.longitude_deg)
        r.insert_into(cur, 'Avion', colonnes, values)
        # print("insert {}".format(avion))
    else:
        # Update avion dans bd
        colonnes = ('nom_config', 'id_aeroport', 'date_derniere_revision',
                    'id_etat', 'latitude_deg', 'longitude_deg')
        values   = (avion.config.nom, avion.aeroport.id_code_iata,
                    avion.date_derniere_revision, avion.etat.value,
                    avion.latitude_deg, avion.longitude_deg)
        r.update(cur, 'Avion', colonnes, values, avion.id)
        # print("update {}".format(avion))
    return


def update_vol(cur, vol):
    """
    Methode qui permet de mettre a jour les informations liées au vol
    
    :param cur: curseur
    :param vol: l'objet vol
    :return: None
    """

    row = r.select_par_id_composite(
        cur, 'Vol', ('id_compagnie', 'numero_vol', 'datetime_depart'),
        (vol.horaire.compagnie.id_code_iata, vol.horaire.numero,
         "{}".format(vol.datetime_depart)))
    id_avion = ''
    if vol.avion:
        id_avion = vol.avion.id
    if not row:
        # Insérer vol dans bd
        colonnes = ('id_compagnie', 'numero_vol',
                    'datetime_depart', 'datetime_arrivee',
                    'duree', 'id_avion',
                    'places_restantes_premiere', 'places_restantes_business',
                    'places_restantes_eco_plus', 'places_restantes_eco',
                    'statut', 'cabine')
        values   = (vol.horaire.compagnie.id_code_iata, vol.horaire.numero,
                    vol.datetime_depart, vol.datetime_arrivee,
                    "{}".format(vol.duree), id_avion,
                    vol.places_restantes_premiere, vol.places_restantes_business,
                    vol.places_restantes_eco_plus, vol.places_restantes_eco,
                    vol.statut.value, vol.cabine)
        r.insert_into(cur, 'Vol', colonnes, values)
        # print("insert {}".format(vol))
    else:
        # Update vol dans bd
        colonnes = ('datetime_depart', 'datetime_arrivee',
                    'duree', 'id_avion', 'places_restantes_premiere',
                    'places_restantes_business', 'places_restantes_eco_plus',
                    'places_restantes_eco', 'statut', 'cabine')
        values   = (vol.datetime_depart, vol.datetime_arrivee,
                    "{}".format(vol.duree), id_avion,
                    vol.places_restantes_premiere, vol.places_restantes_business,
                    vol.places_restantes_eco_plus, vol.places_restantes_eco,
                    vol.statut.value, vol.cabine)
        r.update_composite(
            cur, 'Vol', colonnes, values,
            ('id_compagnie', 'numero_vol', 'datetime_depart'),
            (vol.horaire.compagnie.id_code_iata, vol.horaire.numero,
             "{}".format(vol.datetime_depart)))
        # print("update {}".format(vol))
    return


def update_billet(cur, billet):
    """
    Methode qui permet de mettre a jour les informations liées au billet d'avion
    
    :param cur: curseur
    :param billet: l'objet billet
    :return: None
    """

    row = r.select_par_id(cur, 'Billet', billet.id)
    if not row:
        # Insérer billet dans bd
        colonnes = ('id', 'id_reservation', 'tarif',
                    'nom_passager', 'prenom_passager', 'passeport',
                    'date_naissance', 'options')
        values   = (billet.id, billet.reservation.id, billet.tarif,
                    billet.nom_passager, billet.prenom_passager,
                    billet.passeport, billet.date_naissance,
                    billet.options)
        r.insert_into(cur, 'Billet', colonnes, values)
        # print("insert {}".format(billet))
    else:
        # Update billet dans bd
        colonnes = ('tarif', 'nom_passager', 'prenom_passager',
                    'passeport', 'date_naissance', 'options')
        values   = (billet.tarif, billet.nom_passager,
                    billet.prenom_passager, billet.passeport,
                    billet.date_naissance, billet.options)
        r.update(cur, 'Billet', colonnes, values, billet.id)
        # print("update {}".format(billet))
    return


def update_segment(cur, segment):
    """
    Methode qui permet de mettre a jour les informations liées au segment
    
    :param cur: curseur
    :param segment: l'objet segment
    :return: None
    """

    row = r.select_par_id(cur, 'Segment', segment.id)
    if not row:
        # Insérer segment dans bd
        id_compagnie_codeshare = ""
        numero_vol_codeshare = ""
        if segment.vol.horaire != segment.horaire:
            id_compagnie_codeshare = segment.horaire.compagnie.id_code_iata
            numero_vol_codeshare = segment.horaire.numero
        colonnes = ('id_billet', 'id_compagnie_vol', 'numero_vol',
                    'datetime_vol', 'id_compagnie_codeshare',
                    'numero_vol_codeshare', 'place')
        values   = (segment.billet.id,
                    segment.vol.horaire.compagnie.id_code_iata,
                    segment.vol.horaire.numero,
                    segment.vol.datetime_depart,
                    id_compagnie_codeshare,
                    numero_vol_codeshare,
                    segment.place)
        r.insert_into(cur, 'Segment', colonnes, values)
        # print("insert {}".format(segment))
    else:
        # Update segment dans bd
        colonnes = ('place',)
        values   = (segment.place,)
        r.update(cur, 'Segment', colonnes, values, segment.id)
        # print("update {}".format(segment))
    return
