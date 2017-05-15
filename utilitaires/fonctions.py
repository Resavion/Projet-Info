from datetime import datetime

import ihm.console as ihm


def saisie_date(message, date_seuil, duree_limite=1):
    """
    Methode qui permet de saisir la date du vol
    
    :param message: 
    :param date_seuil: 
    :param duree_limite: 
    :return: la date saisie
    """

    date_saisie = None
    dans1an = date_seuil.replace(year=date_seuil.year + duree_limite)
    while True:
        try:
            date_saisie = ihm.demander(
                "Saisissez la {} (AAAA-MM-JJ) :".format(message))
            date_saisie = datetime.strptime(date_saisie, '%Y-%m-%d')
            if date_saisie <= date_seuil or date_saisie > dans1an:
                raise ValueError
        except ValueError:
            ihm.afficher("Ceci n'est pas une date valide.")
            pass
        else:
            break
    ihm.afficher("Vous avez choisi le {:%d/%m/%Y}".format(date_saisie))
    return date_saisie


def saisie_aeroport(message, aeroports):
    """
    Methode qui permet de saisir un aeroport
    
    :param message: 
    :param aeroports: 
    :return: 
    """

    aero = None
    while aero is None:
        code = ihm.demander(
            "Saisissez l'{} (code IATA ou ICAO ou ville) :".format(message))
        results = [x for x in aeroports
                   if x.id_code_iata == code or x.code_icao == code or
                   x.municipalite.lower().startswith(code)]
        if len(results) == 0:
            ihm.afficher("Désolé, nous n'avons pas trouvé votre aéroport !")
        elif len(results) > 1:
            aero = ihm.choisir_paginer(results, "Précisez votre choix :")
        else:
            aero = results[0]
    ihm.afficher("Vous avez choisi : {}".format(aero))
    return aero


def saisie_compagnie(compagnies):
    """
    Methode qui permet de choisir une compagnie par ses différents codes

    :param compagnies: liste des compagnies
    :return: la compagnie choisie
    """

    compagnie = None
    code = ihm.demander(
        "Tapez le code IATA (2 caractères) ou ICAO (3 caractères) :")
    results = [x for x in compagnies
               if x.id_code_iata == code or x.code_icao == code]
    if len(results) == 0:
        ihm.afficher("Désolé, nous n'avons pas trouvé votre compagnie !")
    else:
        compagnie = results[0]
    if compagnie is not None:
        ihm.afficher("Vous avez choisi la compagnie {}".format(compagnie))
    return compagnie

