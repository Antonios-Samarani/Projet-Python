from src.ingestion import module_1
import src.ingestion as i
filepaths = ["exemple.txt"]

print(list(module_1(filepaths)))

from src.ingestion import module_1  # Code du Module 1
from src.pipeline import (
    nettoyer_flux,
    filtrer_par_severite,
    normaliser_flux,
    analyser_et_router_log
)

LOG_FILE = "exemple.txt"

print(" Début du test du Module 2")

flux_ingere = module_1([LOG_FILE])

flux_propre = nettoyer_flux(flux_ingere)

flux_normalise = normaliser_flux(flux_propre)

count = 0
for log in flux_normalise:
    count += 1
    print(f"\n--- Log #{count} ---")
    print("Dictionnaire normalisé :", log)
    
    analyse = analyser_et_router_log(log)
    print("Résultat match-case     :", analyse)

print(f"\n Test terminé ! Total de logs valides traités : {count}")