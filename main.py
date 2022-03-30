import os
import json

import fire

programmes_folder = '.\programmes'


def load_json(json_path):
    return json.load(open(json_path,"rb"), encoding="utf-8")


def main(candidats='all'):
    # TODO allow selection of candidates
    print("---------------------------------------- Candidats 2022  ----------------------------------------\n")
    print("                        Bienvenue dans cette aide à la décision politique. \n")
    print("Vous devrez attribuer deux notes à 20 mesures par candidat :")
    print("Note 1 : mesure inutile : 0 , ... , 5 : mesure indispensable")
    print("Note 2 : pas du tout d'accord : -5 , ... , 5 : complètement d'accord")

    programme_paths = [os.path.join(programmes_folder, programmes_files)
                       for programmes_files in os.listdir(programmes_folder)]
    
    # Build dict str proposition -> str candidate name
    propositions_dico = {}
    for programme_path in programme_paths:
        dico = load_json(programme_path)
        for proposition in dico["propositions"]:
            propositions_dico[proposition] = dico["name"]
 
    num_propositions = len(propositions_dico)

    # Ask the questions
    # FIXME overkill
    score_by_candidate = {propositions_dico[proposition] : 0 for proposition in propositions_dico.keys()}

    # TODO randomize
    for i, proposition in enumerate(list(propositions_dico.keys())):
        print(f"-------------------- Proposition {i} sur {num_propositions} --------------------")
        print(proposition)
        candidate_name = propositions_dico[proposition]
        importance = input("Importance de la mesure (mesure inutile : 0 , ... , 5 : mesure indispensable) : ")
        accord = input("Accord avec la mesure (pas du tout d'accord : -5 , ... , 5 : complètement d'accord) : ")
        score = float(importance)*float(accord)/25
        score_by_candidate[candidate_name]+=score
        print("\n")

    # Print results
    print("\n")
    print("---------------------------------- Résultats ----------------------------------")
    print("Voici vos scores par candidats (complètement en désaccord : -1 , ... , 1 : complètement en accord)")
    print("\n")

    for candidate_name in list(score_by_candidate.keys()):
        print(f"Candidat : {candidate_name}")
        print(f"score : {score_by_candidate[candidate_name]/20}")
        print("\n")
   
    return


if __name__ == '__main__':
    fire.Fire(main)
