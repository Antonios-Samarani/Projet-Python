def nettoyer_flux(log_stream):
    flux_non_vide = filter(None, log_stream)

    # On vérifie si "severity" est présent dans le dictionnaire,Puisque les logs parsés contiennent obligatoirement la clé "severity"
    return filter(lambda log: type(log) == dict and "severity" in log, flux_non_vide)


def filtrer_par_severite(log_stream, severites_acceptees=("ERROR", "CRITICAL")):
    return filter(lambda log: log.get("severity") in severites_acceptees, log_stream) 

def normaliser_element_log(log) :
    log_clean = log.copy()
    
    if "severity" in log_clean and log_clean["severity"]:
        log_clean["severity"] = log_clean["severity"].upper()
        
    if "message" in log_clean and log_clean["message"]:
        log_clean["message"] = log_clean["message"].strip().lower()
        
    user = log_clean.get("user_id")
    if user is None or user == "":
     user = "ANONYME"

    sev = log_clean.get("severity")
    if sev is None or sev == "":
        sev = "UNKNOWN"

    msg = log_clean.get("message")
    if msg is None or msg == "":
        msg = "aucun message"
    
    log_clean["formatted_summary"] = f"[{sev}] User:{user} -> {msg}"
    
    return log_clean


def normaliser_flux(log_stream):
    return map(normaliser_element_log, log_stream) #map(fonction, iterable) applique la fonction à chaque élément de l'itérable et retourne un itérateur des résultats.


def analyser_et_router_log(log_item):
    match log_item:
        case {"severity": "CRITICAL" | "ERROR", "ip": ip, "message": msg}:
            return f"[ALERTE ERREUR] IP {ip} -> {msg}"
            
        case {"raw": raw_text, "type": "malformed"}:
            return f"[CORROMPU] Ligne brute rejetée : {raw_text}"

        case {"severity": severity, "user_id": user}:
            return f"[LOG STACK] {severity} pour l'utilisateur '{user}'"
            
        case (str(ip), int(port), str(protocol)):
            return f"[RÉSEAU] Connexion immuable : {protocol}://{ip}:{port}"
            
        case str(chaine_brute):
            return f"[TEXTE BRUT] Chaîne non parsée : {chaine_brute}"
            
        case _:
            return "[INCONNU] Format de donnée non reconnu]"