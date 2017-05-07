from bdd.acces_bdd import (ouvrir_connexion,
                           executer_requete,
                           valider_modifs,
                           fermer_connexion)
import bdd.requetes as r


def creer_bdd(db_name):
    """
    Création de la base de données SQLite

    La connexion à la base est refermée à la fin de la fonction.
    """
    conn, cur = ouvrir_connexion(db_name)

    # Création des tables
    req = """create table EnumAvion (id integer primary key AUTOINCREMENT NOT NULL,
                                    etat text)"""
    executer_requete(cur, req)
    req = """create table EnumOption (id integer primary key AUTOINCREMENT NOT NULL,
                                    option text)"""
    executer_requete(cur, req)
    req = """create table EnumStatutVol (id integer primary key AUTOINCREMENT NOT NULL,
                                    statut text)"""
    executer_requete(cur, req)
    req = """create table Aeroport (id text primary key,
                                    type_aero text,
                                    nom text,
                                    latitude_deg real,
                                    longitude_deg real,
                                    elevation_ft integer,
                                    code_continent text,
                                    code_pays text,
                                    municipalite text,
                                    code_icao text,
                                    fuseau text)"""
    executer_requete(cur, req)
    req = """create table Piste (id integer primary key AUTOINCREMENT NOT NULL,
                                 id_aeroport text,
                                 length_ft integer,
                                 le_identificateur text,
                                 le_seuil_decale_ft real,
                                 he_identificateur text,
                                 he_seuil_decale_ft real,
                                 foreign key(id_aeroport) references Aeroport(id))"""
    executer_requete(cur, req)
    req = """create table Compagnie (id text primary key,
                                     nom text,
                                     code_icao text,
                                     pays text,
                                     code_continent text,
                                     code_pays text)"""
    executer_requete(cur, req)
    req = """create table TypeAvion (id text primary key,
                                    code_iata text,
                                    code_icao text,
                                    fuel_cap_L integer,
                                    distance_franchissable_km integer,
                                    vitesse_mach real,
                                    altitude_vol_m integer,
                                    distance_decollage_m integer)"""
    executer_requete(cur, req)
    req = """create table ConfigAvion (id_compagnie text,
                                    nom text,
                                    id_type_avion text,
                                    nb_places_premiere integer,
                                    nb_places_business integer,
                                    nb_places_eco_plus integer,
                                    nb_places_eco integer,
                                    nb_total_places integer,
                                    disposition text,
                                    foreign key(id_compagnie) references Compagnie(id),
                                    foreign key(id_type_avion) references TypeAvion(id),
                                    primary key(id_compagnie,nom))"""
    executer_requete(cur, req)
    req = """create table Avion (id text primary key,
                                 id_compagnie text,
                                 nom_config integer,
                                 id_aeroport text,
                                 date_livraison date,
                                 date_derniere_revision date,
                                 id_etat integer,
                                 position text,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_compagnie,nom_config) references ConfigAvion(id_compagnie,nom),
                                 foreign key(id_aeroport) references Aeroport(id),
                                 foreign key(id_etat) references EnumAvion(id))"""
    executer_requete(cur, req)
    req = """create table Route (id_compagnie text,
                                 id_aeroport_depart text,
                                 id_aeroport_arrivee text,
                                 geom text,
                                 codeshare integer,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_aeroport_depart) references Aeroport(id),
                                 foreign key(id_aeroport_arrivee) references Aeroport(id),
                                 primary key(id_compagnie,id_aeroport_depart,id_aeroport_arrivee))"""
    executer_requete(cur, req)
    req = """create table Horaire (id_compagnie text,
                                 numero_vol integer,
                                 id_aeroport_depart text,
                                 id_aeroport_arrivee text,
                                 id_compagnie_config text,
                                 nom_config text,
                                 heure_depart text,
                                 heure_arrivee text,
                                 duree text,
                                 periodicite text,
                                 id_compagnie_operateur text,
                                 numero_vol_operateur integer,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_compagnie_config) references Compagnie(id),
                                 foreign key(id_compagnie_operateur) references Compagnie(id),
                                 foreign key(id_aeroport_depart) references Aeroport(id),
                                 foreign key(id_aeroport_arrivee) references Aeroport(id),
                                 foreign key(id_compagnie_config,nom_config) references ConfigAvion(id_compagnie,nom),
                                 foreign key(id_compagnie_operateur,numero_vol_operateur) references Horaire(id_compagnie,numero_vol),
                                 primary key(id_compagnie,numero_vol))"""
    executer_requete(cur, req)
    req = """create table Vol (id integer primary key,
                                 id_compagnie text,
                                 numero_vol integer,
                                 datetime_depart text,
                                 datetime_arrivee text,
                                 duree text,
                                 id_avion text,
                                 places_restantes_premiere integer,
                                 places_restantes_business integer,
                                 places_restantes_eco_plus integer,
                                 places_restantes_eco integer,
                                 statut integer,
                                 cabine text,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_compagnie,numero_vol) references Horaire(id_compagnie,numero_vol),
                                 foreign key(id_avion) references Avion(id),
                                 foreign key(statut) references EnumStatutVol(id))"""
    executer_requete(cur, req)
    req = """create table Client (id integer primary key,
                                  nom text,
                                  prenom text,
                                  date_naissance text)"""
    executer_requete(cur, req)
    req = """create table Reservation (id integer primary key,
                                       id_client integer,
                                       prix_total real,
                                       date_achat text,
                                       foreign key(id_client) references Client(id))"""
    executer_requete(cur, req)
    req = """create table Billet (id integer primary key,
                                  id_reservation integer,
                                  tarif real,
                                  nom_passager text,
                                  prenom_passager text,
                                  passeport text,
                                  date_naissance text,
                                  foreign key(id_reservation) references Reservation(id))"""
    executer_requete(cur, req)
    req = """create table Segment (id integer primary key AUTOINCREMENT NOT NULL,
                                   id_billet integer,
                                   id_vol integer,
                                   id_compagnie text,
                                   numero_vol integer,
                                   place text,
                                   foreign key(id_billet) references Billet(id),
                                   foreign key(id_vol) references Vol(id),
                                   foreign key(id_compagnie) references Compagnie(id),
                                   foreign key(id_compagnie,numero_vol) references Horaire(id_compagnie,numero_vol))"""
    executer_requete(cur, req)
    req = """create table BilletOptions (id integer primary key AUTOINCREMENT NOT NULL,
                                   id_billet integer,
                                   id_option integer,
                                   foreign key(id_billet) references Billet(id),
                                   foreign key(id_option) references EnumOption(id))"""
    executer_requete(cur, req)
    req = """create table SegmentOptions (id integer primary key AUTOINCREMENT NOT NULL,
                                   id_segment integer,
                                   id_option integer,
                                   foreign key(id_segment) references Segment(id),
                                   foreign key(id_option) references EnumOption(id))"""
    executer_requete(cur, req)
    valider_modifs(conn)

    fermer_connexion(cur, conn)


def inserer_jeu_test(db_name):
    """
    Insertion des éléments du jeu de données test

    La connexion à la base est refermée à la fin de la fonction.
    """
    conn, cur = ouvrir_connexion(db_name)

    # EnumAvion
    colonnes = ('etat',)
    enumavion = (
        ("en_revision",),
        ("en_vol",),
        ("au_sol",)
    )
    for t in enumavion:
        r.insert_into(cur, 'EnumAvion', colonnes, t)
    valider_modifs(conn)

    # EnumOption
    colonnes = ('option',)
    enumoption = (
        ("vegetarien",),
        ("assurance_annulation",)
    )
    for t in enumoption:
        r.insert_into(cur, 'EnumOption', colonnes, t)
    valider_modifs(conn)

    # EnumStatutVol
    colonnes = ('statut',)
    enumstatutvol = (
        ("a_l_heure",),
        ("retarde",),
        ("embarquement",),
        ("annule",),
        ("arrive",)
    )
    for t in enumstatutvol:
        r.insert_into(cur, 'EnumStatutVol', colonnes, t)
    valider_modifs(conn)

    # Aeroport
    colonnes = ('id','type_aero','nom','latitude_deg','longitude_deg','elevation_ft','code_continent',
                'code_pays','municipalite','code_icao','fuseau')
    aeroports = (
        ("NRT","large_airport","Narita International Airport",35.7647018433,140.386001587,141,"AS","JP","Tokyo","RJAA","Asia/Tokyo"),
        ("KHH","large_airport","Kaohsiung International Airport",22.57710075378418,120.3499984741211, 31,"AS","TW","Kaohsiung City","RCKH","Asia/Taipei"),
        ("BKK","large_airport","Suvarnabhumi Airport",13.681099891662598,100.74700164794922,5,"AS","TH","Bangkok","VTBS","Asia/Bangkok")
    )
    for t in aeroports:
        r.insert_into(cur, 'Aeroport', colonnes, t)
    valider_modifs(conn)

    # Piste
    colonnes = ('id_aeroport','length_ft','le_identificateur','le_seuil_decale_ft','he_identificateur','he_seuil_decale_ft')
    pistes = (
        ("NRT",13123,"16R",'',"34L",2460),
        ("KHH",10335,9,525,27,1477),
        ("BKK",12139,"01L",'',"19R",'')
    )
    for t in pistes:
        r.insert_into(cur, 'Piste', colonnes, t)
    valider_modifs(conn)

    # Compagnie
    colonnes = ('id','nom','code_icao','pays','code_continent','code_pays')
    compagnies = (
        ("BR","EVA Air","EVA","Taiwan","AS","TW"),
        ("CI","China Airlines","CAL","Taiwan","AS","TW"),
        ("NH","All Nippon Airways","ANA","Japan","AS","JP"),
        ("JL","Japan Airlines","JAL","Japan","AS","JP")
    )
    for t in compagnies:
        r.insert_into(cur, 'Compagnie', colonnes, t)
    valider_modifs(conn)

    # TypeAvion
    colonnes = ('id','code_iata','code_icao','fuel_cap_L','distance_franchissable_km','vitesse_mach',
                'altitude_vol_m','distance_decollage_m')
    types = (
        ("A321","321","A321",30000,5950,0.78,12000,1700),
        ("B767-300ER","763","B763",90770,11070,0.8,12000,2400),
        ("B787-9","789","B789",138898,15700,0.85,13000,2900)
    )
    for t in types:
        r.insert_into(cur, 'TypeAvion', colonnes, t)
    valider_modifs(conn)

    # ConfigAvion
    colonnes = ('id_compagnie','nom','id_type_avion','nb_places_premiere','nb_places_business','nb_places_eco_plus',
                'nb_places_eco','nb_total_places','disposition')
    configs = (
        ("BR","321","A321",0,8,0,176,184,""),
        ("JL","A44","B767-300ER",0,24,0,175,199,""),
        ("NH","789","B787-9",0,40,14,192,246,""),
        ("CI","789","B787-9",0,40,14,192,246,"")
    )
    for t in configs:
        r.insert_into(cur, 'ConfigAvion', colonnes, t)
    valider_modifs(conn)

    # Avion
    colonnes = ('id','id_compagnie','nom_config','id_aeroport','date_livraison','date_derniere_revision','id_etat',
                'position')
    avions = (
        ("B-16213","BR","321","KHH","2014-10-10","2014-10-27",3,"POINT(120.3499984741211 22.57710075378418)"),
        ("JA608J","JL","A44","NRT","2004-02-23","2014-05-01",3,"POINT(140.386001587 35.7647018433)"),
        ("JA880A","NH","789","NRT","2016-07-28","2016-07-28",3,"POINT(140.386001587 35.7647018433)"),
        ("B-18666","CI","789","KHH","2016-07-28","2016-07-28",3,"POINT(120.3499984741211 22.57710075378418)")
    )
    for t in avions:
        r.insert_into(cur, 'Avion', colonnes, t)
    valider_modifs(conn)

    # Route
    colonnes = ('id_compagnie','id_aeroport_depart','id_aeroport_arrivee','geom','codeshare')
    routes = (
        ("BR","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0),
        ("NH","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0),
        ("JL","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0),
        ("CI","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0),
        ("NH","NRT","BKK","LINESTRING(140.386001587 35.7647018433,2.54999995232 49.0127983093)",0),
        ("NH","BKK","NRT","LINESTRING(100.747001647949 13.6810998916626,140.386001587 35.7647018433)",0),
        ("CI","BKK","KHH","LINESTRING(100.747001647949 13.6810998916626,120.349998474121 22.5771007537842)",0),
        ("NH","BKK","KHH","LINESTRING(100.747001647949 13.6810998916626,120.3499984741 22.5771007538)",1)
    )
    for t in routes:
        r.insert_into(cur, 'Route', colonnes, t)
    valider_modifs(conn)

    # Horaire
    colonnes = ('id_compagnie','numero_vol','id_aeroport_depart','id_aeroport_arrivee',
                'id_compagnie_config','nom_config',
                'heure_depart','heure_arrivee','duree','periodicite',
                'id_compagnie_operateur','numero_vol_operateur')
    horaires = (
        ("BR",107,"NRT","KHH","BR","321","12:45","15:40","3h55",None,None,None),
        ("NH",5831,"NRT","KHH",None,None,None,None,None,None,"BR",107),
        ("JL",811,"NRT","KHH","JL","A44","18:00","21:10","4h10",None,None,None),
        ("CI",9911,"NRT","KHH",None,None,None,None,None,None,"JL",811),
        ("NH",807,"NRT","BKK","NH","789","16:55","21:35","6h40",None,None,None),
        ("NH",808,"BKK","NRT","NH","789","00:30","08:40","5h50",None,None,None),
        ("CI",840,"BKK","KHH","NH","789","18:35","22:55","3h32",None,None,None),
        ("NH",9940,"BKK","KHH",None,None,None,None,None,None,"CI",840),
    )
    for t in horaires:
        r.insert_into(cur, 'Horaire', colonnes, t)
    valider_modifs(conn)

    # Vol
    colonnes = ('id','id_compagnie','numero_vol',
                'datetime_depart','datetime_arrivee','duree','id_avion',
                'places_restantes_premiere','places_restantes_business',
                'places_restantes_eco_plus','places_restantes_eco','statut')
    vols = (
        (1,"BR",107,"2017-04-27 12:50:00","2017-04-27 15:50:00","4:00:00","B-16213",0,3,0,76,5),
        (2,"JL",811,"2017-04-27 18:00:00","2017-04-27 21:10:00","4:10:00","JA608J",0,10,0,100,5),
        (3,"NH",807,"2017-04-27 16:55:00","2017-04-27 21:35:00","6:40:00","JA880A",0,10,0,100,5),
        (4,"NH",808,"2017-04-28 00:30:00","2017-04-28 08:40:00","5:50:00","JA880A",0,10,0,100,5),
        (5,"CI",840,"2017-04-28 18:35:00","2017-04-27 22:55:00","3:32:00","B-18666",0,10,0,100,5)
    )
    for t in vols:
        r.insert_into(cur, 'Vol', colonnes, t)
    valider_modifs(conn)

    # Client
    colonnes = ('id','nom','prenom','date_naissance')
    clients = (
        (1,"Dupond","Michel","1970-04-10"),
        (2,"Tartempion","Lucien","1960-03-20"),
    )
    for t in clients:
        r.insert_into(cur, 'Client', colonnes, t)
    valider_modifs(conn)

    # Reservation
    colonnes = ('id','id_client','prix_total','date_achat')
    resas = (
        (1,1,1300,"2017-04-20 23:59:59"),
        (2,1,500,"2017-04-19 13:40:01"),
    )
    for t in resas:
        r.insert_into(cur, 'Reservation', colonnes, t)
    valider_modifs(conn)

    # Billet
    colonnes = ('id','id_reservation','tarif','nom_passager','prenom_passager','passeport','date_naissance')
    billets = (
        (10001,1,1200,"Chaffouin","Antoine","123456D","1980-05-15"),
        (20002,2,400,"Tartempion","Lucien","123789E","1960-03-20"),
    )
    for t in billets:
        r.insert_into(cur, 'Billet', colonnes, t)
    valider_modifs(conn)

    # Segment
    colonnes = ('id_billet','id_vol','id_compagnie','numero_vol','place')
    segments = (
        (10001,1,"NH",5831,"36A"),
        (20002,2,None,None,"45H"),
    )
    for t in segments:
        r.insert_into(cur, 'Segment', colonnes, t)
    valider_modifs(conn)

    # BilletOptions
    colonnes = ('id_billet','id_option')
    billetoptions = (
        (10001,2),
    )
    for t in billetoptions:
        r.insert_into(cur, 'BilletOptions', colonnes, t)
    valider_modifs(conn)

    # SegmentOptions
    colonnes = ('id_segment','id_option')
    segmentoptions = (
        (1,1),
    )
    for t in segmentoptions:
        r.insert_into(cur, 'SegmentOptions', colonnes, t)
    valider_modifs(conn)

    fermer_connexion(cur, conn)


def inserer_jeu_fichiers(db_name):
    """
    Insertion des éléments du jeu de données a partir des fichiers

    La connexion à la base est refermée à la fin de la fonction.
    """
    conn, cur = ouvrir_connexion(db_name)

    # EnumAvion
    colonnes = ('etat',)
    enumavion = (
        ("en_revision",),
        ("en_vol",),
        ("au_sol",)
    )
    for t in enumavion:
        r.insert_into(cur, 'EnumAvion', colonnes, t)
    valider_modifs(conn)

    # EnumOption
    colonnes = ('option',)
    enumoption = (
        ("vegetarien",),
        ("assurance_annulation",)
    )
    for t in enumoption:
        r.insert_into(cur, 'EnumOption', colonnes, t)
    valider_modifs(conn)

    # EnumStatutVol
    colonnes = ('statut',)
    enumstatutvol = (
        ("a_l_heure",),
        ("retarde",),
        ("embarquement",),
        ("annule",),
        ("arrive",)
    )
    for t in enumstatutvol:
        r.insert_into(cur, 'EnumStatutVol', colonnes, t)
    valider_modifs(conn)

    r.insert_from_file(cur, 'data/aeroports.csv', 'Aeroport')
    r.insert_from_file(cur, 'data/pistes.csv', 'Piste')
    r.insert_from_file(cur, 'data/compagnies.csv', 'Compagnie')
    r.insert_from_file(cur, 'data/types_avions.csv', 'TypeAvion')
    r.insert_from_file(cur, 'data/configs_avions.csv', 'ConfigAvion')
    r.insert_from_file(cur, 'data/avions.csv', 'Avion')
    r.insert_from_file(cur, 'data/routes.csv', 'Route')
    valider_modifs(conn)

    fermer_connexion(cur, conn)


if __name__ == '__main__':
    import os
    os.remove("resavion.db")
    creer_bdd("resavion.db")
    inserer_jeu_test("resavion.db")
    # inserer_jeu_fichiers("resavion.db")
