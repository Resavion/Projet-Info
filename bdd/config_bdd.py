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
                                    statut text)"""
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
    req = """create table TypeAvion (id integer primary key AUTOINCREMENT NOT NULL,
                                    nb_place_premiere integer,
                                    nb_place_business integer,
                                    nb_place_eco_plus integer,
                                    nb_place_eco integer,
                                    nb_total_place integer,
                                    fuel_cap_L integer,
                                    distance_franchissable_km integer,
                                    coefficient_cout real,
                                    vitesse_mach real,
                                    altitude_vol_m integer,
                                    distance_decollage_m integer)"""
    executer_requete(cur, req)
    req = """create table Avion (id integer primary key AUTOINCREMENT NOT NULL,
                                 date_construction date,
                                 date_derniere_revision date,
                                 etat integer,
                                 id_compagnie text,
                                 id_aeroport text,
                                 id_type_avion integer,
                                 position text,
                                 foreign key(etat) references EnumAvion(id),
                                 foreign key(id_compagnie) references Compagnie(id_iata_code),
                                 foreign key(id_aeroport) references Aeroport(id_iata_code),
                                 foreign key(id_type_avion) references TypeAvion(id))"""
    executer_requete(cur, req)
    req = """create table Route (id integer primary key AUTOINCREMENT NOT NULL,
                                 id_compagnie text,
                                 id_aeroport_depart text,
                                 id_aeroport_arrivee text,
                                 geom text,
                                 distance real,
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
    colonnes = ('id_iata_code','type','nom','latitude_deg','longitude_deg','elevation_ft','continent','pays','municipalite','gps_code')
    aeroports = (
        ("NRT","large_airport","Narita International Airport",35.7647018433,140.386001587,141,"AS","JP","Tokyo","RJAA"),
        ("KHH", "large_airport","Kaohsiung International Airport",22.57710075378418,120.3499984741211, 31,"AS","TW","Kaohsiung City","RCKH")
    )
    for t in aeroports:
        r.insert_into(cur, 'Aeroport', colonnes, t)
    valider_modifs(conn)

    colonnes = ('id_aeroport','length_ft','le_identificateur','le_seuil_decale_ft','he_identificateur','he_seuil_decale_ft')
    pistes = (
        ("NRT",13123,"16R",'',"34L",2460),
        ("KHH",10335,9,525,27,1477)
    )
    for t in pistes:
        r.insert_into(cur, 'Piste', colonnes, t)
    valider_modifs(conn)

    colonnes = ('id_iata_code','nom','icao_code','pays')
    compagnies = (
        ("NH","All Nippon Airways","ANA","Japan"),
        ("CI","China Airlines","CAL","Taiwan")
    )
    for t in compagnies:
        r.insert_into(cur, 'Compagnie', colonnes, t)
    valider_modifs(conn)

#18768,1,"CI","NRT",,"35.7647018433","140.386001587"
#18768,2,"CI","KHH",,"22.5771007538","120.3499984741"
#7632,1,"NH","NRT",,"35.7647018433","140.386001587"
#7632,2,"NH","KHH",,"22.5771007538","120.3499984741"
    fermer_connexion(cur, conn)


if __name__ == '__main__':
    creer_bdd("resavion.db")
