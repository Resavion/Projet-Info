import sqlite3


def ouvrir_connexion(db_name):
    """
    Connexion à une base de données
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return conn, cur


def executer_requete(cur, req, variables=()):
    """
    Requête à la base de données
    """
    cur.execute(req, variables)


def valider_modifs(conn):
    """
    Valider la transaction
    """
    conn.commit()


def fermer_connexion(cur, conn):
    """
    Fermeture de la connexion
    """
    cur.close()
    conn.close()


