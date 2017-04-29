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
    rows = r.select_all(cur, 'Compagnie')
    for row in rows:
        compagnie = Compagnie(*row)
        # Configs
        configs = charger_configs_par_compagnie(cur, types_avions, compagnie)
        compagnie.configs.extend(configs)
        # Avions
        avions = charger_avions_par_compagnie(cur, aeroports, configs, compagnie)
        compagnie.avions.extend(avions)
        # Routes
        print(compagnie)
        compagnies.append(compagnie)

    # # Routes
    # routes = charger_routes(cur, aeroports, avions, configs)

    # # Horaires
    # horaires = charger_horaires(cur, configs)

    # # Vols
    # vols = charger_vols(cur, horaires, avions)


def charger_aeroports(cur):
    rows = r.select_all(cur, 'Aeroport')
    aeroports = []
    for row in rows:
        id_aeroport = row[0]
        # Pistes
        rows_pistes = r.select_pistes_par_aeroport(cur, id_aeroport)
        pistes = []
        for row_piste in rows_pistes:
            piste = Piste(*row_piste)
            pistes.append(piste)
            # print(piste)
        aeroport = Aeroport(*row, pistes)
        aeroports.append(aeroport)
        # print(aeroport)
    return aeroports


def charger_types_avions(cur):
    rows = r.select_all(cur,'TypeAvion')
    types_avions = []
    for row in rows:
        type_avion = TypeAvion(*row)
        types_avions.append(type_avion)
        # print(type_avion)
    return types_avions


def charger_configs_par_compagnie(cur, types_avions, compagnie):
    configs = []
    rows = r.select_all_par_compagnie(cur,'ConfigAvion',compagnie.id_compagnie)
    for row in rows:
        type_avion = [x for x in types_avions if x.id_type_avion == row[3]][0]
        config = ConfigAvion(*row[0:2], compagnie, type_avion, *row[4:])
        configs.append(config)
        # print(config)
    return configs


def charger_avions_par_compagnie(cur, aeroports, configs, compagnie):
    avions = []
    rows = r.select_all_par_compagnie(cur,'Avion',compagnie.id_compagnie)
    for row in rows:
        config = [x for x in configs if x.id_config_avion == row[2]][0]
        aeroport = [x for x in aeroports if x.id_aero == row[3]][0]
        date_construc = datetime.strptime(row[4],"%d/%m/%Y").date()
        date_der_rev = datetime.strptime(row[5],"%d/%m/%Y").date()
        avion = Avion(row[0], compagnie, config, aeroport,
                      date_construc, date_der_rev, *row[6:])
        avions.append(avion)
        # print(avion)
    return avions


def charger_routes(cur, aeroports, avions, configs):
    routes = []
    rows = r.select_all(cur, 'Route')
    for row in rows:
        id_route = row[0]
        dep = [x for x in aeroports if x.id_aero == row[2]][0]
        arr = [x for x in aeroports if x.id_aero == row[3]][0]
        route = Route(id_route,row[1],dep,arr,row[4],row[5],None)
        print(route)
    return routes


def charger_horaires(cur, configs):
    horaires = []
    rows = r.select_horaires_pas_codeshare(cur)
    for row in rows:
        print(row)
        id_config = row[9]
        config = [x for x in configs if x.id_config_avion == id_config][0]
        dep = datetime.strptime(row[4],"%H:%M").time()
        arr = datetime.strptime(row[5],"%H:%M").time()
        t = datetime.strptime(row[6],"%H:%M")
        dur = timedelta(hours=t.hour, minutes=t.minute)
        horaire = Horaire(*row[0:4],dep,arr,dur,*row[7:-1],config)
        horaires.append(horaire)
        print(horaire)
    rows = r.select_horaires_codeshare(cur)
    for row in rows:
        id_horaire_operateur = row[8]
        horaire_operateur = [x for x in horaires if x.id_horaire == id_horaire_operateur][0]
        horaire = Horaire(*row[0:8], horaire_operateur, None)
        horaires.append(horaire)
        print(horaire)
    return horaires


def charger_vols(cur, horaires, avions):
    vols = []
    rows = r.select_all(cur, 'Vol')
    for row in rows:
        id_horaire = row[1]
        horaire = [x for x in horaires if x.id_horaire == id_horaire][0]
        id_avion = row[5]
        avion = [x for x in avions if x.id_avion == id_avion][0]
        dep = datetime.strptime(row[2],"%d/%m/%Y-%H:%M")
        arr = datetime.strptime(row[3],"%d/%m/%Y-%H:%M")
        vol = Vol(row[0],horaire,dep,arr,*row[4:5],avion,*row[6:])
        print(vol)
    return vols


def charger_horaires_de_route(cur, id_route, types_avions):
    rows = r.select_horaires_par_route(cur, id_route)
    horaires = []
    for row in rows:
        print(row)
        # Config
        id_config = row[9]
        config = None
        if id_config:
            config = charger_config_par_id(cur, id_config, types_avions)
        # Horaire
        horaire = Horaire(*row[0:-1],config)
        print(horaire)
        horaires.append(horaire)
    return horaires


def charger_config_par_id(cur, id_config, types_avions):
    row_config = r.select_config_par_id(cur, id_config)
    id_type_avion = row_config[3]
    type_avion = [x for x in types_avions if x.id_type_avion == id_type_avion][0]
    config = ConfigAvion(*row_config[0:3], type_avion, *row_config[4:])
    return config


# def initialiser_partie(db_name):
#     """
#     Créer un joueur humain et lui affecter un pokemon
#
#     :param db_name: chemin de la base
#     :return: le joueur humain
#     :returntype: DresseurHumain
#     """
#     nom_dresseur = ihm.demander("Choisir un nom de dresseur : ")
#     nom_espece = ihm.choisir(["Bulbizare", "Salamèche", "Carapuce"],
#                              "Choisir un pokemon pour votre dresseur : ")
#     nom_pokemon = ihm.demander("Choisir un nom pour ce pokemon : ")
#
#     conn, cur = ouvrir_connexion(db_name)
#
#     colonnes = ('force', 'defense', 'pv', 'type_pok')
#     row = r.select_esp_pok_by_nom(cur, colonnes, nom_espece)
#     espece = EspecePokemon(nom_espece, row[3], row[0], row[1], row[2])
#
#     valider_modifs(conn)
#     fermer_connexion(cur, conn)
#
#     attaque = Attaque("Charge", 40, "Normal", 100)
#     if nom_espece == "Bulbizare":
#         attaque_spe = Attaque("Fouet liane", 45, "Plante", 100)
#     elif nom_espece == "Salamèche":
#         attaque_spe = Attaque("Flammèche", 40, "Feu", 100)
#     else:
#         attaque_spe = Attaque("Hydrocanon", 110, "Eau", 80)
#
#     pokemon = Pokemon(nom_pokemon, espece, [attaque, attaque_spe], 3)
#     joueur = DresseurHumain(nom_dresseur, [pokemon])
#     ihm.logger("Partie initialisée")
#     return joueur
#
#
# def sauvegarder_partie(db_name, joueur):
#     """
#     Sauvegarde une partie dans la bdd
#
#     :param db_name: nom de la base de données où sauvegarder la partie
#     :param joueur: DresseurHumain de la partie
#     """
#     pass
#
#
# def jouer(joueur, dresseurs, pokemons):
#     """
#     Boucle de jeu
#
#     :param joueur: le dresseur humain
#     :param dresseurs: les dresseurs contrôlés par l'ordinateur
#     :param pokemons: pokemons sauvages
#     :return:
#     """
#     victoire = True
#
#     while victoire:
#         action = ihm.demander("Tapez sur une touche pour passer au tour suivant ou q pour quitter ")
#         if action == 'q':
#             break
#
#         action = randint(0, 4)
#         if action == 0:
#             msg = "{} se promène tranquillement. Il ne se passe rien de spécial.".format(joueur)
#             ihm.afficher(msg)
#
#         elif action in [1, 2]:
#             pokemon_sauvage = pokemons[randint(0, len(pokemons)-1)]
#             msg = "{} rencontre un {} sauvage. Que faire ?".format(joueur, pokemon_sauvage.espece)
#             liste_choix = ["L'attaquer", "Le capturer", "S'enfuir"]
#             choix = ihm.choisir(liste_choix, msg)
#             if choix == "L'attaquer":
#                 victoire = joueur.defier_sauvage(pokemon_sauvage)
#             elif choix == "Le capturer":
#                 try:
#                     nouveau_nom = pokemon_sauvage.nom
#                     while nouveau_nom in [p.nom for p in pokemons] or nouveau_nom in [p.nom for p in joueur.pokemons]:
#                         nouveau_nom = ihm.demander("Choisir un nom pour le pokemon capturé : ")
#                     joueur.capturer(pokemon_sauvage, nouveau_nom)
#                 except ValueError as e:
#                     ihm.afficher(e)
#             else:
#                 ihm.afficher("{} s'enfuit.".format(joueur))
#
#         else:
#             msg = "{} rencontre un autre dresseur. Que faire ?".format(joueur)
#             liste_choix = ["Le défier", "Continuer son chemin"]
#             choix = ihm.choisir(liste_choix, msg)
#             if choix == "Le défier":
#                 dresseur = dresseurs[randint(0, len(dresseurs)-1)]
#                 victoire = joueur.defier(dresseur)
#             else:
#                 ihm.afficher("{} continue sa route.".format(joueur))
#
#     else:
#         ihm.afficher("GAME OVER")
