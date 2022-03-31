import os
import random

import fire

from candidat import Candidat


def load_candidats(programmes_folder = '.\candidats'):
    programme_paths = [os.path.join(programmes_folder, programmes_files)
            for programmes_files in os.listdir(programmes_folder)]
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


def main():
    """
    Main script, ask the selection of candidates, ask the questions and print results.
    """

    # Load candidates' profiles
    candidats = load_candidats()

    # Intro
    print("---------------------------------------- Candidats 2022  ----------------------------------------\n")
    print("                        Bienvenue dans cette aide à la décision politique. \n")
    print("Vous devrez attribuer deux notes à chaque mesure des candidats choisis :")
    print("Note 1 : mesure inutile : 0 , ... , 5 : mesure indispensable")
    print("Note 2 : pas du tout d'accord : -5 , ... , 5 : complètement d'accord")
    print("\n")

    name = input("Votre nom : ")
    print("\n")
    
    # Candidates selection
    print("Veuillez choisir les candidats desquels vous voulez juger les propositions,")
    print("sous la forme d'une chaîne de caractères des diminutifs des candidats, séparés par '-'.")
    print("\n")

    print("Exemple : 'ma-me-ro' pour Macron, Méenchon, Roussel).")
    print("Pour juger les programmes de tous les candidats, appuyez sur Entrée.")
    print("\n")

    print("Diminutif des candidats :")
    for candidat in candidats:
        print(f"{candidat.name} : {candidat.nickname}")
    print("\n")

    valid_input = False
    while not valid_input:
        selection_candidats = input("Choix des candidats : ")
        valid_input, selected_candidats_nicknames = split_selection_candidats(selection_candidats, candidats)

    # Filter the candidats list based on selection
    selected_candidats = [candidat for candidat in candidats if candidat.nickname in selected_candidats_nicknames]
    print("\n")

    print("Les candidats choisis sont :")
    for candidat in selected_candidats:
        print(f"{candidat.name},")
    print("\n")

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

    for i, proposition in enumerate(proposition_keys):
        print(
            f"-------------------- Proposition {i+1} sur {num_propositions} --------------------")
        print(proposition)
        print("\n")
        candidate_name = propositions_dico[proposition]
        importance = input_float(
            "Importance de la mesure (mesure inutile : 0 , ... , 5 : mesure indispensable) : ")
        accord = input_float(
            "Accord avec la mesure (pas du tout d'accord : -5 , ... , 5 : complètement d'accord) : ")
        score = float(importance)*float(accord)/25
        score_by_candidate[candidate_name] += score
        print("\n")

    print("Félicitation, vous avez terminé !")
    input("Appuyez sur Entrée pour voir vos résultats")

    # Print results
    print("\n")
    print("---------------------------------- Résultats ----------------------------------")
    print(
        f"Voici les scores de {name} par candidats (complètement en désaccord : -1 , ... , 1 : complètement en accord) :")
    print("\n")

    # TODO print results in descending order of score
    for candidat in selected_candidats:
        candidate_name = candidat.name
        print(f"{candidate_name} : {score_by_candidate[candidate_name]/candidat.num_propositions}")


    # TODO allow saving the results in a e.g. txt file
    # TODO add matplotlib dependency and save a plot

    return


if __name__ == '__main__':
    fire.Fire(main)
