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
    req = """create table Aeroport (id integer primary key,
                                    identifiant text,
                                    type text,
                                    nom text,
                                    latitude real,
                                    longitude real,
                                    elevation integer,
                                    continent text,
                                    pays text,
                                    municipalite text,
                                    gps_code text,
                                    iata_code text)"""
    executer_requete(cur, req)
    req = """create table Piste (id integer primary key,
                                 id_aeroport integer,
                                 identifiant_aeroport text,
                                 length_ft integer,
                                 le_identificateur text,
                                 le_seuil_decale_ft real,
                                 he_identificateur text,
                                 he_seuil_decale_ft real,
                                 foreign key(id_aeroport) references Aeroport(id))"""
    executer_requete(cur, req)
    req = """create table Compagnie (id integer primary key,
                                     nom text,
                                     alias text,
                                     iata text,
                                     icao text,
                                     callsign text,
                                     pays text,
                                     actif text)"""
    executer_requete(cur, req)
    req = """create table TypeAvion (id integer primary key,
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
                                    distance_decollage_m integer,
                                    etops integer)"""
    executer_requete(cur, req)
    req = """create table Avion (id integer primary key,
                                 date_construction date,
                                 date_derniere_revision date,
                                 etat integer,
                                 id_compagnie integer
                                 id_aeroport integer,
                                 id_type_avion integer,
                                 position text,
                                 statut EnumAvion,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_aeroport) references Aeroport(id),
                                 foreign key(id_type_avion) references TypeAvion(id))"""
    executer_requete(cur, req)
    req = """create table Route (id integer primary key,
                                 id_compagnie integer,
                                 id_aeroport_depart integer,
                                 id_aeroport_arrivee integer,
                                 geom text,
                                 distance real,
                                 codeshare integer,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_aeroport_depart) references Aeroport(id),
                                 foreign key(id_aeroport_arrivee) references Aeroport(id))"""
    executer_requete(cur, req)
    req = """create table Horaire (id integer primary key,
                                 numero integer,
                                 id_compagnie integer,
                                 id_route integer,
                                 heure_depart text,
                                 heure_arrivee text,
                                 duree text,
                                 periodicite text,
                                 id_horaire_operateur integer,
                                 id_type_avion integer,
                                 foreign key(id_compagnie) references Compagnie(id),
                                 foreign key(id_route) references Route(id),
                                 foreign key(id_horaire_operateur) references Horaire(id),
                                 foreign key(id_type_avion) references TypeAvion(id))"""
    executer_requete(cur, req)
    req = """create table Vol (id integer primary key,
                                 id_horaire integer,
                                 heure_depart text,
                                 heure_arrivee text,
                                 id_avion integer,
                                 places_restantes_premiere integer,
                                 places_restantes_business integer,
                                 places_restantes_eco_plus integer,
                                 places_restantes_eco integer,
                                 statut EnumStatutVol,
                                 foreign key(id_horaire) references Horaire(id),
                                 foreign key(id_avion) references Avion(id))"""
    executer_requete(cur, req)
    req = """create table Client (id integer primary key,
                                  nom text,
                                  prenom text,
                                  date_naissance text)"""
    executer_requete(cur, req)
    req = """create table Reservation (id text primary key,
                                       id_client integer,
                                       prix_total real,
                                       foreign key(id_client) references Client(id))"""
    executer_requete(cur, req)
    req = """create table Billet (id integer primary key,
                                  id_reservation text,
                                  options EnumOption,
                                  tarif real,
                                  nom_passager text,
                                  prenom_passager text,
                                  passeport text,
                                  date_naissance text,
                                  foreign key(id_reservation) references Reservation(id))"""
    executer_requete(cur, req)
    req = """create table Segment (id_billet integer,
                                   id_vol integer,
                                   primary key(id_billet, id_vol),
                                   place text,
                                   options EnumOption,
                                   foreign key(id_billet) references Billet(id),
                                   foreign key(id_vol) references Vol(id))"""
    executer_requete(cur, req)
    valider_modifs(conn)
    # 
    # # Insertion des éléments
    # types = ('Normal', 'Feu', 'Eau', 'Plante', 'Electrique')
    # for t in types:
    #     r.insert_into(cur, 'TypePok', ('nom',), (t,))
    # valider_modifs(conn)
    # 
    # dresseurs = ('Dresseur 1', 'Dresseur 2', 'Dresseur 3', 'Dresseur 4', 'Dresseur 5')
    # for d in dresseurs:
    #     r.insert_into(cur, 'Dresseur', ('nom', 'type'), (d, 2))
    # valider_modifs(conn)
    # 
    # attaques = (
    #     ('Eclair', 40, 100, 'Electrique'),
    #     ('Poing éclair', 75, 100, 'Electrique'),
    #     ('Fatal foudre', 110, 70, 'Electrique'),
    #     ('Fouet liane', 45, 100, 'Plante'),
    #     ('Méga-sangsue', 40, 100, 'Plante'),
    #     ("Tranch'Herbe", 55, 95, 'Plante'),
    #     ('Charge', 40, 100, 'Normal'),
    #     ('Morsure', 60, 100, 'Normal'),
    #     ('Jet-Pierres', 50, 90, 'Normal'),
    #     ('Bélier', 90, 85, 'Normal'),
    #     ('Coupe', 50, 95, 'Normal'),
    #     ('Croc de mort', 80, 90, 'Normal'),
    #     ('Hydrocanon', 110, 80, 'Eau'),
    #     ('Hydroblast', 150, 90, 'Eau'),
    #     ('Ocroupi', 95, 85, 'Eau'),
    #     ('Danse flamme', 35, 85, 'Feu'),
    #     ('Flammèche', 40, 100, 'Feu'),
    #     ('Lance-flammes', 90, 100, 'Feu')
    # )
    # colonnes = ('nom', 'puissance', 'precision', 'type_pok')
    # for att in attaques:
    #     r.insert_into(cur, 'Attaque', colonnes, att)
    # valider_modifs(conn)
    # 
    # especes = (
    #     ('Bulbizare', 49, 49, 45, 'Plante'),
    #     ('Salamèche', 52, 43, 39, 'Feu'),
    #     ('Carapuce', 48, 65, 44, 'Eau'),
    #     ('Pikachu', 55, 40, 35, 'Electrique'),
    #     ('Chenipan', 30, 35, 45, 'Normal'),
    #     ('Rattata', 56, 35, 30, 'Normal'),
    #     ('Piafabec', 60, 30, 40, 'Normal'),
    #     ('Tentacool', 40, 35, 40, 'Eau'),
    #     ('Mystherbe', 50, 55, 45, 'Plante'),
    #     ('Voltali', 65, 60, 65, 'Electrique')
    # )
    # colonnes = ('nom', 'force', 'defense', 'pv', 'type_pok')
    # for esp in especes:
    #     r.insert_into(cur, 'EspecePokemon', colonnes, esp)
    # valider_modifs(conn)
    # 
    # pokemons = (
    #     ('Bulbi sauvage', 'Bulbizare', 'Dresseur 1'),
    #     ('Pika sauvage', 'Pikachu', 'Dresseur 1'),
    #     ('Rattata sauvage', 'Rattata', 'Dresseur 2'),
    #     ('Chenipan sauvage', 'Chenipan', 'Dresseur 3'),
    #     ('Piaf sauvage', 'Piafabec', 'Dresseur 3'),
    #     ('Pieuvre des mers', 'Tentacool', 'Dresseur 4'),
    #     ('Mystherbe sauvage', 'Mystherbe', 'Dresseur 5'),
    #     ('Voltali sauvage', 'Voltali', 'Dresseur 5')
    # )
    # colonnes = ('nom', 'espece', 'dresseur')
    # for pok in pokemons:
    #     r.insert_into(cur, 'Pokemon', colonnes, pok)
    # valider_modifs(conn)
    # 
    # pok_att = (
    #     ('Bulbi sauvage', 'Charge'),
    #     ('Bulbi sauvage', 'Fouet liane'),
    #     ('Bulbi sauvage', "Tranch'Herbe"),
    #     ('Pika sauvage', 'Charge'),
    #     ('Pika sauvage', 'Eclair'),
    #     ('Rattata sauvage', 'Morsure'),
    #     ('Rattata sauvage', 'Croc de mort'),
    #     ('Chenipan sauvage', 'Charge'),
    #     ('Piaf sauvage', 'Coupe'),
    #     ('Piaf sauvage', 'Jet-Pierres'),
    #     ('Pieuvre des mers', 'Hydroblast'),
    #     ('Pieuvre des mers', 'Hydrocanon'),
    #     ('Pieuvre des mers', 'Ocroupi'),
    #     ('Mystherbe sauvage', 'Méga-sangsue'),
    #     ('Mystherbe sauvage', "Tranch'Herbe"),
    #     ('Voltali sauvage', 'Poing éclair'),
    #     ('Voltali sauvage', 'Fatal foudre'),
    #     ('Voltali sauvage', 'Charge')
    # )
    # colonnes = ('nom_pok', 'nom_att')
    # for pa in pok_att:
    #     r.insert_into(cur, 'PokemonAtt', colonnes, pa)
    # valider_modifs(conn)

    fermer_connexion(cur, conn)


if __name__ == '__main__':
    creer_bdd("pokemon.db")
