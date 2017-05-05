import csv

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


def insert_from_file(cur, filename, table, delim=';'):
    with open(filename, 'r', newline='', encoding='utf-8') as infh:
        rows = list(csv.reader(infh, delimiter=delim))
        col = rows[0]
        for row in rows[1:]:
            insert_into(cur, table, col, row)
