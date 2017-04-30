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
                                    code_icao text)"""
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
    req = """create table ConfigAvion (id integer primary key,
                                    nom text,
                                    id_compagnie text,
                                    id_type_avion text,
                                    nb_place_premiere integer,
                                    nb_place_business integer,
                                    nb_place_eco_plus integer,
                                    nb_place_eco integer,
                                    nb_total_place integer,
                                    disposition text,
                                    foreign key(id_compagnie) references Compagnie(id),
                                    foreign key(id_type_avion) references TypeAvion(id))"""
    executer_requete(cur, req)
    req = """create table Avion (id text primary key,
                                 id_compagnie text,
                                 id_config integer,
                                 id_aeroport text,
                                 date_construction date,
                                 date_derniere_revision date,
                                 id_etat integer,
                                 position text,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_config) references ConfigAvion(id),
                                 foreign key(id_aeroport) references Aeroport(id),
                                 foreign key(id_etat) references EnumAvion(id))"""
    executer_requete(cur, req)
    req = """create table Route (id integer primary key,
                                 id_compagnie text,
                                 id_aeroport_depart text,
                                 id_aeroport_arrivee text,
                                 geom text,
                                 codeshare integer,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_aeroport_depart) references Aeroport(id),
                                 foreign key(id_aeroport_arrivee) references Aeroport(id))"""
    executer_requete(cur, req)
    req = """create table Horaire (id integer primary key,
                                 id_route integer,
                                 id_compagnie text,
                                 numero_vol integer,
                                 heure_depart text,
                                 heure_arrivee text,
                                 duree text,
                                 periodicite text,
                                 id_horaire_operateur integer,
                                 id_config_avion integer,
                                 foreign key(id_route) references Route(id),
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_horaire_operateur) references Horaire(id),
                                 foreign key(id_config_avion) references ConfigAvion(id))"""
    executer_requete(cur, req)
    req = """create table Vol (id integer primary key,
                                 id_horaire integer,
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
                                 foreign key(id_horaire) references Horaire(id),
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
                                  options text,
                                  foreign key(id_reservation) references Reservation(id))"""
    executer_requete(cur, req)
    req = """create table Segment (id integer primary key AUTOINCREMENT NOT NULL,
                                   id_billet integer,
                                   id_vol integer,
                                   id_horaire integer,
                                   place text,
                                   option EnumOption,
                                   foreign key(id_billet) references Billet(id),
                                   foreign key(id_vol) references Vol(id),
                                   foreign key(id_horaire) references Horaire(id))"""
    executer_requete(cur, req)
    valider_modifs(conn)

    # Insertion des éléments

    # EnumAvion
    colonnes = ('etat',)
    enumavion = (
        ("en revision",),
        ("en vol",),
        ("a terre",)
    )
    for t in enumavion:
        r.insert_into(cur, 'EnumAvion', colonnes, t)
    valider_modifs(conn)

    # EnumOption
    colonnes = ('option',)
    enumoption = (
        ("vegetarien",)
    )
    for t in enumavion:
        r.insert_into(cur, 'EnumOption', colonnes, t)
    valider_modifs(conn)

    # EnumStatutVol
    colonnes = ('statut',)
    enumstatutvol = (
        ("a l'heure",),
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
                'code_pays','municipalite','code_icao')
    aeroports = (
        ("NRT","large_airport","Narita International Airport",35.7647018433,140.386001587,141,"AS","JP","Tokyo","RJAA"),
        ("KHH", "large_airport","Kaohsiung International Airport",22.57710075378418,120.3499984741211, 31,"AS","TW","Kaohsiung City","RCKH")
    )
    for t in aeroports:
        r.insert_into(cur, 'Aeroport', colonnes, t)
    valider_modifs(conn)

    # Piste
    colonnes = ('id_aeroport','length_ft','le_identificateur','le_seuil_decale_ft','he_identificateur','he_seuil_decale_ft')
    pistes = (
        ("NRT",13123,"16R",'',"34L",2460),
        ("KHH",10335,9,525,27,1477)
    )
    for t in pistes:
        r.insert_into(cur, 'Piste', colonnes, t)
    valider_modifs(conn)

    # Compagnie
    colonnes = ('id','nom','code_icao','pays','code_continent','code_pays')
    compagnies = (
        ("NH","All Nippon Airways","ANA","Japan","AS","JP"),
        ("BR","EVA Air","EVA","Taiwan","AS","TW"),
        ("CI","China Airlines","CAL","Taiwan","AS","TW"),
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
        ("B767-300ER","763","B763",90770,11070,0.8,12000,2400)
    )
    for t in types:
        r.insert_into(cur, 'TypeAvion', colonnes, t)
    valider_modifs(conn)

    # ConfigAvion
    colonnes = ('id','nom','id_compagnie','id_type_avion','nb_place_premiere','nb_place_business','nb_place_eco_plus',
                'nb_place_eco','nb_total_place','disposition')
    configs = (
        (1,"321","BR","A321",0,8,0,176,184,""),
        (2,"A44","JL","B767-300ER",0,24,0,175,199,"")
    )
    for t in configs:
        r.insert_into(cur, 'ConfigAvion', colonnes, t)
    valider_modifs(conn)

    # Avion
    colonnes = ('id','id_compagnie','id_config','id_aeroport','date_construction','date_derniere_revision','id_etat',
                'position')
    avions = (
        ("B-16213","BR",1,"KHH","2014-10-10","2014-10-27",3,"POINT(120.3499984741211 22.57710075378418)"),
        ("JA608J","JL",2,"NRT","2004-02-23","2014-05-01",3,"POINT(140.386001587 35.7647018433)")
    )
    for t in avions:
        r.insert_into(cur, 'Avion', colonnes, t)
    valider_modifs(conn)

    # Route
    colonnes = ('id','id_compagnie','id_aeroport_depart','id_aeroport_arrivee','geom','codeshare')
    routes = (
        (1,"BR","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0),
        (2,"NH","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0),
        (3,"JL","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0),
        (4,"CI","NRT","KHH","LINESTRING(140.386001587 35.7647018433,120.3499984741 22.5771007538)",0)
    )
    for t in routes:
        r.insert_into(cur, 'Route', colonnes, t)
    valider_modifs(conn)

    # Horaire
    colonnes = ('id','id_route','id_compagnie','numero_vol','heure_depart','heure_arrivee','duree',
                'periodicite','id_horaire_operateur','id_config_avion')
    horaires = (
        (1,1,"BR",107,"12:45","15:40","3:55",None,None,1),
        (2,2,"NH",5831,None,None,None,None,1,None),
        (3,3,"JL",811,"18:00","21:10","4:10",None,None,2),
        (4,4,"CI",9911,None,None,None,None,3,None)
    )
    for t in horaires:
        r.insert_into(cur, 'Horaire', colonnes, t)
    valider_modifs(conn)

    # Vol
    colonnes = ('id','id_horaire','datetime_depart','datetime_arrivee','duree','id_avion','places_restantes_premiere',
                'places_restantes_business','places_restantes_eco_plus','places_restantes_eco','statut')
    vols = (
        (1,1,"27/04/2017-12:50","27/04/2017-15:50","4:00","B-16213",0,3,0,76,5),
        (2,3,"27/04/2017-18:00","27/04/2017-21:10","4:10","JA608J",0,10,0,100,5),
    )
    for t in vols:
        r.insert_into(cur, 'Vol', colonnes, t)
    valider_modifs(conn)

    # Client
    colonnes = ('id','nom','prenom','date_naissance')
    clients = (
        (1,"Dupond","Michel","10/04/1970"),
        (2,"Tartempion","Lucien","20/03/1960"),
    )
    for t in clients:
        r.insert_into(cur, 'Client', colonnes, t)
    valider_modifs(conn)

    # Reservation
    colonnes = ('id','id_client','prix_total','date_achat')
    resas = (
        (1,1,1300,"20/04/2017-23:59:59"),
        (2,2,500,"19/04/2017-13:40:01"),
    )
    for t in resas:
        r.insert_into(cur, 'Reservation', colonnes, t)
    valider_modifs(conn)

    # Billet
    colonnes = ('id','id_reservation','tarif','nom_passager','prenom_passager','passeport','date_naissance','options')
    billets = (
        (10001,1,1200,"Chaffouin","Antoine","123456D","15/05/1980",None),
        (20002,2,400,"Tartempion","Lucien","123789E","20/03/1960",None),
    )
    for t in billets:
        r.insert_into(cur, 'Billet', colonnes, t)
    valider_modifs(conn)

    # Segment
    colonnes = ('id_billet','id_vol','id_horaire','place','option')
    segments = (
        (10001,1,2,"36A",1),
        (20002,2,3,"45H",None),
    )
    for t in segments:
        r.insert_into(cur, 'Segment', colonnes, t)
    valider_modifs(conn)

    fermer_connexion(cur, conn)


if __name__ == '__main__':
    import os
    os.remove("resavion.db")
    creer_bdd("resavion.db")
