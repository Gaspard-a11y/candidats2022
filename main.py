import os
import json
import random

import fire
from tqdm import tqdm

from candidat import Candidat


def load_candidats(programmes_dir = '.\candidats'):
    programme_paths = [os.path.join(programmes_dir, programmes_files)
            for programmes_files in os.listdir(programmes_dir)]
    candidats = [Candidat(programme_path) for programme_path in programme_paths]
    return candidats


def split_selection_candidats(string, candidats):
    """
    Split the input string into a list of candidats' nicknames, return the list.
    Return whether the input is valid.
    Input string : e.g. 'ma-me-ro'
    Input candidats = list of Candidat objects.
    """
    candidats_nicknames = [candidat.nickname for candidat in candidats]
    if len(string)==0:
        valid_input = True
        return valid_input, candidats_nicknames
    else :
        valid_input = True
        selected_nicknames = string.lower().split('-')
        # Check that all nicknames are registered
        for selected_nickname in selected_nicknames:
            valid_input &= (selected_nickname in candidats_nicknames)
        return valid_input, selected_nicknames


def input_float(prompt):
    """
    Input a float number in str format.
    Empty float results in 0.
    """
    string = input(prompt)
    if len(string)==0:
        return 0.
    else:
        return float(string)


def main(output_dir = u'.\resultats'):
    """
    Main script, ask the selection of candidates, ask the questions and print results.
    """

    # Load candidates' profiles
    candidats = load_candidats()

    # Intro
    print("---------------------------------------- Candidats 2022  ----------------------------------------\n")
    print("                        Bienvenue dans cette aide à la décision politique. \n")
    print("Vous devrez attribuer une note à chaque mesure des candidats choisis :")
    print("-5 = complètement en désaccord, ... , 0 = Indifférent , ... , 5 : complètement d'accord")
    print("\n")

    name = input("Votre prénom : ")
    print("\n")
    
    # Candidates selection
    print("Veuillez choisir les candidats desquels vous voulez juger les propositions,")
    print("sous la forme d'une chaîne de caractères des diminutifs des candidats, séparés par '-'.")
    print("\n")

    print("Exemple : 'ma-me-ro' pour Macron, Méenchon, Roussel).")
    print("Pour juger les programmes de tous les candidats, appuyez sur Entrée.")
    print("\n")

    names_and_nicknames = [f"{candidat.name} : {candidat.nickname}" for candidat in candidats]
    prompt = '\n'.join(names_and_nicknames)
    print(f"Diminutif des candidats :\n{prompt}\n")

    valid_input = False
    while not valid_input:
        selection_candidats = input("Choix des candidats : ")
        valid_input, selected_candidats_nicknames = split_selection_candidats(selection_candidats, candidats)

    # Filter the candidats list based on selection
    selected_candidats = [candidat for candidat in candidats if candidat.nickname in selected_candidats_nicknames]
    print("\n")

    selected_names = [f"{candidat.name}" for candidat in selected_candidats]
    prompt = '\n'.join(selected_names)
    print(f"Les candidats choisis sont :\n{prompt}\n")

    input("Appuyer sur Entrée pour commencer.")
    print("\n")


    # Build dict str proposition -> str candidate name
    propositions_dico = {}
    for candidat in selected_candidats:
        for proposition in candidat.propositions:
            propositions_dico[proposition] = candidat.name
    num_propositions = len(propositions_dico)

    # Shuffle the propositions
    proposition_keys = list(propositions_dico)
    random.shuffle(proposition_keys)

    # Ask the questions
    score_by_candidate = {
        candidat.name : 0. for candidat in selected_candidats}

    for proposition in tqdm(proposition_keys, desc="Progression"):
        print("--------------------------------------------------------------------------------------------------")
        print(proposition)
        print("\n")
        candidate_name = propositions_dico[proposition]
        accord = input_float(
            "Accord avec la mesure (pas du tout d'accord : -5 , ... , 5 : complètement d'accord) : ")
        score = float(accord)/5
        score_by_candidate[candidate_name] += score
        print("\n")

    print("\n")
    print("---------------------------------------- C'est terminé !  ----------------------------------------\n")
    input("Appuyez sur Entrée pour voir vos résultats")

    # Print results
    print("\n")
    print("---------------------------------- Résultats ----------------------------------")
    print(
        f"Voici les scores de {name} par candidats (complètement en désaccord : -1 , ... , 1 : complètement en accord) :")
    print("\n")

    # Average out each score
    for candidat in selected_candidats:
        score_by_candidate[candidat.name] /= candidat.num_propositions

    # Print the results in descending order
    sorted_scores = list(score_by_candidate.items())
    sorted_scores.sort(reverse=True, key = lambda x: x[1])
    for name_score in sorted_scores:
        candidate_name, score = name_score
        print(f"{candidate_name} : {round(score,2)}")
    print("\n")

#    output_path = output_dir + '\' + name + '.json'
#    json_object = json.dumps(score_by_candidate, indent = 4)
#    with open(output_path, "w") as outfile:
#        outfile.write(json_object)
    
    # TODO allow saving the results in a e.g. txt file
    # TODO add matplotlib dependency and save a plot

    return


if __name__ == '__main__':
    fire.Fire(main)
