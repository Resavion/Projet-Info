from random import randint

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

    rows = r.select_aeroports(cur)
    aeroports = []
    for row in rows:
        id_aeroport = row[0]
        rows_pistes = r.select_pistes_par_aeroport(cur, id_aeroport)
        pistes = []
        for row_piste in rows_pistes:
            piste = Piste(*row_piste)
            pistes.append(piste)
            print(piste)
        aeroport = Aeroport(*row, pistes)
        print(aeroport)


#
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
