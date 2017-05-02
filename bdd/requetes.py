from bdd.acces_bdd import executer_requete


def insert_into(cur, table, col, values):
    req = "INSERT INTO {} (".format(table)
    req += ", ".join(col)
    req += ") VALUES ("
    req += ", ".join(['?' for i in values])
    req += ");"
    executer_requete(cur, req, values)


def update(cur, table, col, values, id_objet):
    req = "UPDATE {} SET ".format(table)
    req += "=?, ".join(col)
    req += "=? WHERE id='{}'".format(id_objet)
    req += ";"
    executer_requete(cur, req, values)


def select_all(cur, table):
    req = "SELECT * FROM "+table
    executer_requete(cur, req)
    return cur.fetchall()


def select_all_par_compagnie(cur, table, id_compagnie):
    req = "SELECT * FROM "+table+" WHERE id_compagnie = ?"
    executer_requete(cur, req, (id_compagnie,))
    return cur.fetchall()


def select_par_id(cur, table, id_objet):
    req = "SELECT * FROM "+table+" WHERE id = ?"
    executer_requete(cur, req, (id_objet,))
    return cur.fetchall()


def select_pistes_par_aeroport(cur, id_aero):
    req = "SELECT * FROM Piste WHERE id_aeroport = ?"
    executer_requete(cur, req, (id_aero,))
    return cur.fetchall()


def select_horaires_propres_par_route(cur, id_route):
    req = "SELECT * FROM Horaire WHERE id_horaire_operateur IS NULL"
    req += " AND id_route = ?"
    executer_requete(cur, req, (id_route,))
    return cur.fetchall()


def select_horaires_codeshare_par_route(cur, id_route):
    req = "SELECT * FROM Horaire WHERE id_horaire_operateur IS NOT NULL"
    req += " AND id_route = ?"
    executer_requete(cur, req, (id_route,))
    return cur.fetchall()


def select_vols_par_horaire(cur, id_horaire):
    req = "SELECT * FROM Vol WHERE id_horaire = ?"
    executer_requete(cur, req, (id_horaire,))
    return cur.fetchall()


def select_resas_par_client(cur, id_client):
    req = "SELECT * FROM Reservation WHERE id_client = ?"
    executer_requete(cur, req, (id_client,))
    return cur.fetchall()


def select_billets_par_resa(cur, id_resa):
    req = "SELECT * FROM Billet WHERE id_reservation = ?"
    executer_requete(cur, req, (id_resa,))
    return cur.fetchall()


def select_options_par_billet(cur, id_billet):
    req = "SELECT id_option FROM BilletOptions WHERE id_billet = ?"
    executer_requete(cur, req, (id_billet,))
    return cur.fetchall()


def select_segments_par_billet(cur, id_billet):
    req = "SELECT * FROM Segment WHERE id_billet = ?"
    executer_requete(cur, req, (id_billet,))
    return cur.fetchall()


def select_options_par_segment(cur, id_segment):
    req = "SELECT id_option FROM SegmentOptions WHERE id_segment = ?"
    executer_requete(cur, req, (id_segment,))
    return cur.fetchall()

#
# def select_esp_pok_by_nom(cur, colonnes, nom_espece):
#     req = "SELECT "
#     req += ", ".join(colonnes)
#     req += " FROM EspecePokemon WHERE nom = ?"
#     executer_requete(cur, req, (nom_espece,))
#     return cur.fetchone()
#
#
# def select_dresseurs_by_type(cur, type_dresseur):
#     req = "SELECT * FROM Dresseur WHERE type = ?"
#     executer_requete(cur, req, (type_dresseur,))
#     return cur.fetchall()
#
#
# def select_dresseur_by_nom(cur, nom_dresseur):
#     req = "SELECT * FROM Dresseur WHERE nom = ?"
#     executer_requete(cur, req, (nom_dresseur,))
#     return cur.fetchone()
#
#
# def select_pokemons_by_dresseur(cur, nom_dresseur):
#     req = "SELECT * FROM Pokemon WHERE dresseur = ?"
#     executer_requete(cur, req, (nom_dresseur,))
#     return cur.fetchall()
#
#
# def select_pokemon_by_nom(cur, nom_pok):
#     req = "SELECT * FROM Pokemon WHERE nom = ?"
#     executer_requete(cur, req, (nom_pok,))
#     return cur.fetchone()
#
#
# def select_attaques_by_pokemon(cur, nom_pok):
#     req = "SELECT A.* FROM Attaque A JOIN PokemonAtt P ON nom_att = A.nom WHERE nom_pok = ?"
#     executer_requete(cur, req, (nom_pok,))
#     return cur.fetchall()
