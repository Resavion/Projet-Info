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
    req = """create table EnumSatutVol (id integer primary key AUTOINCREMENT NOT NULL,
                                    statut text)"""
    executer_requete(cur, req)
    req = """create table Aeroport (id_iata_code text primary key,
                                    type text,
                                    nom text,
                                    latitude_deg real,
                                    longitude_deg real,
                                    elevation_ft integer,
                                    continent text,
                                    pays text,
                                    municipalite text,
                                    gps_code text)"""
    executer_requete(cur, req)
    req = """create table Piste (id integer primary key AUTOINCREMENT NOT NULL,
                                 id_aeroport text,
                                 length_ft integer,
                                 le_identificateur text,
                                 le_seuil_decale_ft real,
                                 he_identificateur text,
                                 he_seuil_decale_ft real,
                                 foreign key(id_aeroport) references Aeroport(id_iata_code))"""
    executer_requete(cur, req)
    req = """create table Compagnie (id_iata_code text primary key,
                                     nom text,
                                     icao_code text,
                                     pays text)"""
    executer_requete(cur, req)
    req = """create table TypeAvion (id text primary key,
                                    iata_code text,
                                    icao_code text,
                                    fuel_cap_L integer,
                                    distance_franchissable_km integer,
                                    vitesse_mach real,
                                    altitude_vol_m integer,
                                    distance_decollage_m integer)"""
    executer_requete(cur, req)
    req = """create table ConfigAvion (id text,
                                    id_compagnie text,
                                    primary key(nom, id_compagnie),
                                    id_type_avion text,
                                    nb_place_premiere integer,
                                    nb_place_business integer,
                                    nb_place_eco_plus integer,
                                    nb_place_eco integer,
                                    nb_total_place integer,
                                    disposition text,
                                    foreign key(id_compagnie) references Compagnie(id_iata_code),
                                    foreign key(id_type_avion) references TypeAvion(id))"""
    executer_requete(cur, req)
    req = """create table Avion (id_reg text primary key,
                                 id_compagnie text,
                                 id_config integer,
                                 date_construction date,
                                 date_derniere_revision date,
                                 etat integer,
                                 id_aeroport text,
                                 position text,
                                 foreign key(etat) references EnumAvion(id),
                                 foreign key(id_compagnie) references Compagnie(id_iata_code),
                                 foreign key(id_config, id_compagnie) references ConfigAvion(id, id_compagnie),
                                 foreign key(id_aeroport) references Aeroport(id_iata_code))"""
    executer_requete(cur, req)
    req = """create table Route (id integer primary key AUTOINCREMENT NOT NULL,
                                 id_compagnie text,
                                 id_aeroport_depart text,
                                 id_aeroport_arrivee text,
                                 geom text,
                                 codeshare integer,
                                 foreign key(id_compagnie) references Compagnie(id_iata_code),
                                 foreign key(id_aeroport_depart) references Aeroport(id_iata_code),
                                 foreign key(id_aeroport_arrivee) references Aeroport(id_iata_code))"""
    executer_requete(cur, req)
    req = """create table Horaire (id integer primary key AUTOINCREMENT NOT NULL,
                                 id_compagnie text,
                                 numero_vol integer,
                                 id_route integer,
                                 heure_depart text,
                                 heure_arrivee text,
                                 duree text,
                                 periodicite text,
                                 id_horaire_operateur integer,
                                 id_type_avion integer,
                                 foreign key(id_compagnie) references Compagnie(id_iata_code),
                                 foreign key(id_route) references Route(id),
                                 foreign key(id_horaire_operateur) references Horaire(id),
                                 foreign key(id_type_avion) references TypeAvion(id))"""
    executer_requete(cur, req)
    req = """create table Vol (id integer primary key AUTOINCREMENT NOT NULL,
                                 id_horaire integer,
                                 heure_depart text,
                                 heure_arrivee text,
                                 id_avion integer,
                                 places_restantes_premiere integer,
                                 places_restantes_business integer,
                                 places_restantes_eco_plus integer,
                                 places_restantes_eco integer,
                                 statut integer,
                                 foreign key(id_horaire) references Horaire(id),
                                 foreign key(id_avion) references Avion(id),
                                 foreign key(statut) references EnumStatutVol(id))"""
    executer_requete(cur, req)
    req = """create table Client (id integer primary key AUTOINCREMENT NOT NULL,
                                  nom text,
                                  prenom text,
                                  date_naissance text)"""
    executer_requete(cur, req)
    req = """create table Reservation (id integer primary key AUTOINCREMENT NOT NULL,
                                       id_client integer,
                                       prix_total real,
                                       foreign key(id_client) references Client(id))"""
    executer_requete(cur, req)
    req = """create table Billet (id integer primary key AUTOINCREMENT NOT NULL,
                                  id_reservation integer,
                                  option text,
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
                                   place text,
                                   options EnumOption,
                                   foreign key(id_billet) references Billet(id),
                                   foreign key(id_vol) references Vol(id))"""
    executer_requete(cur, req)
    valider_modifs(conn)

    # Insertion des éléments

    # EnumAvion
    colonnes = ('etat')
    enumavion = (
        ("en revision"),
        ("en vol"),
        ("a terre")
    )
    for t in enumavion:
        r.insert_into(cur, 'EnumAvion', colonnes, t)
    valider_modifs(conn)

    # EnumOption
    colonnes = ('option')
    enumavion = (
        ("vegetarien")
    )
    for t in enumavion:
        r.insert_into(cur, 'EnumAvion', colonnes, t)
    valider_modifs(conn)

    # EnumStatutVol
    colonnes = ('statut')
    enumavion = (
        ("a l'heure"),
        ("retarde"),
        ("embarquement"),
        ("annule")
    )
    for t in enumavion:
        r.insert_into(cur, 'EnumAvion', colonnes, t)
    valider_modifs(conn)

    # Aeroport
    colonnes = ('id_iata_code','type','nom','latitude_deg','longitude_deg','elevation_ft','continent','pays',
                'municipalite','gps_code')
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
    colonnes = ('id_iata_code','nom','icao_code','pays')
    compagnies = (
        ("NH","All Nippon Airways","ANA","Japan"),
        ("BR", "EVA Air", "EVA", "Taiwan"),
        ("CI","China Airlines","CAL","Taiwan"),
        ("JL","Japan Airlines","JAL","Japan")
    )
    for t in compagnies:
        r.insert_into(cur, 'Compagnie', colonnes, t)
    valider_modifs(conn)

    # TypeAvion
    colonnes = ('nom','iata_code','icao_code','fuel_cap_L','distance_franchissable_km','vitesse_mach',
                'altitude_vol_m','distance_decollage_m')
    types = (
        ("A321","321","A321",30000,5950,0.78,12000,1700),
        ("B767-300ER","763","B763",90770,11070,0.8,12000,2400)
    )
    for t in types:
        r.insert_into(cur, 'TypeAvion', colonnes, t)
    valider_modifs(conn)

    # ConfigAvion
    colonnes = ('nom','id_compagnie','id_type_avion','nb_place_premiere','nb_place_business','nb_place_eco_plus',
                'nb_place_eco','nb_total_place','disposition')
    configs = (
        ("321","BR","A321",0,8,0,176,184,""),
        ("A44","JL","B767-300ER",0,24,0,175,199,"")
    )
    for t in configs:
        r.insert_into(cur, 'ConfigAvion', colonnes, t)
    valider_modifs(conn)

    # Avion
    colonnes = ('id_reg','id_compagnie','id_config','date_construction','date_derniere_revision','etat','id_aeroport',
                'position')
    configs = (
        ("B-16213","BR","321","10/10/2014","27/10/2014",3,"KHH","POINT(120.3499984741211 22.57710075378418)"),
        ("JA608J","JL","A44","23/02/2004","01/05/2014",3,"NRT","POINT(140.386001587 35.7647018433)")
    )
    for t in configs:
        r.insert_into(cur, 'ConfigAvion', colonnes, t)
    valider_modifs(conn)

    # Route
    colonnes = ('id_compagnie', 'id_aeroport_depart', 'id_aeroport_arrivee', 'geom', 'codeshare')
    routes = (
        ("NH", "NRT", "KHH", "LINESTRING(140.386001587 35.7647018433, 120.3499984741 22.5771007538)", 0),
        ("CI", "NRT", "KHH", "LINESTRING(140.386001587 35.7647018433, 120.3499984741 22.5771007538)", 0)
    )
    for t in routes:
        r.insert_into(cur, 'Route', colonnes, t)
    valider_modifs(conn)

    # Horaire
    colonnes = ('id_compagnie','numero_vol','id_route','heure_depart','heure_arrivee','duree','periodicite',
                'id_horaire_operateur','id_type_avion')
    horaires = (
        ("NH",5831, "KHH", "LINESTRING(140.386001587 35.7647018433, 120.3499984741 22.5771007538)", 0),
        ("CI", "NRT", "KHH", "LINESTRING(140.386001587 35.7647018433, 120.3499984741 22.5771007538)", 0)
    )
    for t in horaires:
        r.insert_into(cur, 'Horaire', colonnes, t)
    valider_modifs(conn)

    fermer_connexion(cur, conn)


if __name__ == '__main__':
    import os
    os.remove("resavion.db")
    creer_bdd("resavion.db")
