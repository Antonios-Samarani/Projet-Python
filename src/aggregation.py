# defaultdict c'est un dictionnaire qui renvoie 0 si y'a pas de clé
# On en a besoin pour lister les tentatives vu qu'on les a pas à l'avance
from collections import defaultdict

# c'est la fonction qui vas lire tout ce que le module 1 lui envoie et le stocker dans des sets
# On cherche à compter les ips actives, les ips avec erreur, le nombre d'occurence de chaque niveau, le nombre d'occurence de chaque utilisateur et à stocker les tentatives de connexion par ip
def collecter(d): # records c'est tout ce qu'on recoit de module 1/ le flux de dictionnaires du log
    # on declare les variables ou on va stocker
    ips_actives = set()
    ips_erreur = set()
    par_niveau = defaultdict(int) #on cherche à compter le nombre d'occurence de chaque niveau avec un truc du genre {"INFO": 10, "ERROR": 5, "Warning": 2}
    par_utilisateur = defaultdict(int)
    tentatives = defaultdict(list)

    for record in d:
        # dans le cas ou le log est mal formé on skip
        if record.get("type") == "malformed":
            continue # continue skip le reste de la boucle et passe à l'itération d'apres 

        # On lit tout
        ip = record["ip"]
        niveau = record["severity"]
        utilisateur = record["user_id"]
        message = record["message"]

        if message is None:
            message = ""

        ips_actives.add(ip) # on remplie les ips du coup

        # pareil pour les ips avec erreurs
        if niveau == "ERROR" or niveau == "CRITICAL":
            ips_erreur.add(ip) 

        par_niveau[niveau] += 1 # on complete aussi les niveaux pour avoir le nombre d'occurence de chaque niveau

        # pareil pour les utilisateurs on compte le nombre d'occurence de chaque utilisateur
        if utilisateur is not None:
            par_utilisateur[utilisateur] += 1

        # on sotcke les tentatives de connexion et leur reussite ou echec pour chaque ip
        if "Échec" in message:
            tentatives[ip].append(False)
        elif "Connexion réussie" in message:
            tentatives[ip].append(True)

    return ips_actives, ips_erreur, par_niveau, par_utilisateur, tentatives # on revoie nos 5 données du coup


# on la determine arbitrairement ici mais on peut la changer si on veut
BLACKLIST = frozenset({"10.0.0.66", "10.0.0.99", "10.0.0.50"})
# On applique juste les différentes opperations qui sont demandées et on mets tout dans un set resulats qu'on return
def compare_blacklist(ips_actives, blacklist):
    r = {}
    r["union"] = ips_actives | blacklist
    r["intersection"] = ips_actives & blacklist
    r["actives_seulement"] = ips_actives - blacklist
    r["blacklist_seulement"] = blacklist - ips_actives
    r["difference_symetrique"] = ips_actives ^ blacklist
    return r


# Avec ce code on vas tester si un utilisateur utilise du brut force ( en gros il spam )
# ca consiste juste à compter pour chaque ip son nombre de tentatives fausses en traversant le tableau de ses tentatives et de comparer ca à un seuil ici 5
# pour definir si c'est une attaque ou pas
def bruteforce(tentatives):
    # on vas noter les ips des personnes qui essayent d'attaquer dans des listes du coup
    ips_attaquantes = []
    ips_sans_attaque = []

    for ip in tentatives:
        resultats = tentatives[ip] # pour economiser un peu de ram ( c'est le tableau des tentatives )
        echecs_consecutifs = 0
        i = 0

        # on compte vraiment simplement avec un while et des comparaisons avec 5 tout simplement
        while i < len(resultats):
            if resultats[i] == True:
                echecs_consecutifs = 0
                i += 1
                continue

            echecs_consecutifs += 1
            i += 1
            if echecs_consecutifs >= 5:
                ips_attaquantes.append(ip)
                break
        else:
            ips_sans_attaque.append(ip)

    return ips_attaquantes, ips_sans_attaque

# on appelle juste toutes les fonctons osef et on return un set avec toutes les infos qu'on cherchais pour se module
def module3(records, blacklist=BLACKLIST):
    ips_actives, ips_erreur, par_niveau, par_utilisateur, tentatives = collecter(records)

    resultat = {}
    resultat["ips_erreur"] = ips_erreur
    resultat["par_niveau"] = dict(par_niveau)
    resultat["par_utilisateur"] = dict(par_utilisateur)
    resultat["blacklist"] = compare_blacklist(ips_actives, blacklist)
    attaquantes, saines = bruteforce(tentatives)
    resultat["force_brute"] = attaquantes
    resultat["sans_attaque"] = saines
    return resultat

