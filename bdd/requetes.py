from bdd.acces_bdd import executer_requete


def insert_into(cur, table, col, values):
    req = "INSERT INTO {} (".format(table)
    req += ", ".join(col)
    req += ") VALUES ("
    req += ", ".join(['?' for i in values])
    req += ");"
    executer_requete(cur, req, values)


def update(cur, table, col, values, nom):
    req = "UPDATE {} SET ".format(table)
    req += "=?, ".join(col)
    req += "=? WHERE nom='{}'".format(nom)
    req += ";"
    executer_requete(cur, req, values)


def select_all(cur, table):
    req = "SELECT * FROM "+table
    executer_requete(cur, req)
    return cur.fetchall()


def select_pistes_par_aeroport(cur, id_aero):
    req = "SELECT * FROM Piste WHERE id_aeroport = ?"
    executer_requete(cur, req, (id_aero,))
    return cur.fetchall()


def select_avions_par_compagnie(cur, id_compagnie):
    req = "SELECT * FROM Avion WHERE id_compagnie = ?"
    executer_requete(cur, req, (id_compagnie,))
    return cur.fetchall()


def select_routes_par_compagnie(cur, id_compagnie):
    req = "SELECT * FROM Route WHERE id_compagnie = ?"
    executer_requete(cur, req, (id_compagnie,))
    return cur.fetchall()


def select_horaires_par_route(cur, id_route):
    req = "SELECT * FROM Horaire WHERE id_route = ?"
    executer_requete(cur, req, (id_route,))
    return cur.fetchall()


def select_horaires_pas_codeshare(cur):
    req = "SELECT * FROM Horaire WHERE id_horaire_operateur IS NULL"
    executer_requete(cur, req)
    return cur.fetchall()


def select_horaires_codeshare(cur):
    req = "SELECT * FROM Horaire WHERE id_horaire_operateur IS NOT NULL"
    executer_requete(cur, req)
    return cur.fetchall()


def select_config_par_id(cur, id_config):
    req = "SELECT * FROM ConfigAvion WHERE id = ?"
    executer_requete(cur, req, (id_config,))
    return cur.fetchone()

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
