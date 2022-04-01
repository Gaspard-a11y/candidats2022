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


def input_float(prompt): # TODO add min & max
    """
    Input a float number in str format.
    Empty float results in 0.
    """
    string = input(prompt)
    if len(string)==0:
        return 0.
    else:
        return float(string)


def save_object_into_json(item, output_path):
    with open(output_path, 'w', encoding='utf8') as json_file:
        json.dump(item, json_file, ensure_ascii=False, indent=4)
    return


def main(output_dir = './resultats'):
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

    # Check if there already are results
    output_path = output_dir + '/' + name + '.json'
    if os.path.exists(output_path):
        reuse_input = input("Des résultats à ce nom ont été trouvés, les compléter ? (Si 'N', les résultats précédents seront écrasés) [Y/N] : ").lower()
        if reuse_input=='y' or reuse_input=='yes' or reuse_input=='o' or reuse_input=='oui':
            reuse_input = True
        elif reuse_input=='n' or reuse_input=='no' or reuse_input=='non':
            reuse_input = False
        else :
            reuse_input = True

    # Candidates selection
    print("\n")
    print("Veuillez choisir les candidats desquels vous voulez juger les propositions,")
    print("sous la forme d'une chaîne de caractères des diminutifs des candidats, séparés par '-'.")
    print("\n")

    print("Exemple : 'ma-me-ro' pour Macron, Méenchon, Roussel).")
    print("Pour juger les programmes de tous les candidats, appuyez sur Entrée.")
    if reuse_input:
        print("Si vous notez à nouveau un candidat, son score précédent sera écrasé.")
    print("\n")

    names_and_nicknames = [f"{candidat.name} : {candidat.nickname}" for candidat in candidats]
    prompt = '\n'.join(names_and_nicknames)
    print(f"Diminutif des candidats :\n{prompt}\n")

    valid_input = False
    while not valid_input:
        selection_candidats = input("Choix des candidats : ")
        valid_input, selected_candidats_nicknames = split_selection_candidats(selection_candidats, candidats)
        if not valid_input:
            print("Sélection incorrecte, veuillez réessayer.")

    # Filter the candidats list based on selection
    selected_candidats = [candidat for candidat in candidats if candidat.nickname in selected_candidats_nicknames]

    selected_names = [f"{candidat.name}" for candidat in selected_candidats]
    prompt = '\n'.join(selected_names)
    print(f"Les candidats choisis sont :\n{prompt}\n")

    input("Appuyer sur Entrée pour commencer.\n")

    # Build dict str proposition -> str candidate name
    propositions_dico = {}
    for candidat in selected_candidats:
        for proposition in candidat.propositions:
            propositions_dico[proposition] = candidat.name

    # Shuffle the propositions
    proposition_keys = list(propositions_dico)
    random.shuffle(proposition_keys)

    # Initialize scores
    if reuse_input:
        # Read the previous json file
        score_by_candidate = json.load(open(output_path, "rb"), encoding="utf-8")
        # Re-initialize the scores of the selected candidates
        for candidat in selected_candidats:
            score_by_candidate[candidat.name] = 0.
    else:
        score_by_candidate = {candidat.name : 0. for candidat in selected_candidats}

    # Ask the questions
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

    print("\n---------------------------------------- C'est terminé !  ----------------------------------------\n")
    input("Appuyez sur Entrée pour voir vos résultats.")

    # Print results
    print("\n---------------------------------- Résultats ----------------------------------\n")
    prompt = ', '.join(selected_names)
    print(f"Les candidats qui ont été notés sont : {prompt}.")
    print(f"Voici les scores de {name} par candidats (complètement en désaccord : -1 , ... , 1 : complètement en accord) :\n")

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

    # Save the results in a json file
    save_object_into_json(score_by_candidate, output_path)
    print(f"Résultats sauvegardés à : {output_path}\n")

    # TODO add matplotlib dependency and save a plot

    return


if __name__ == '__main__':
    fire.Fire(main)
