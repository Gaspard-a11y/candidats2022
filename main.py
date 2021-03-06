import os
import json
import random
from pathlib import Path

import fire
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from candidat import Candidat


def load_candidats(programmes_dir_path=Path('candidats/')):
    programmes_dir_path = Path(programmes_dir_path)
    # programme_paths = [os.path.join(programmes_dir_path, programmes_files)
    #                    for programmes_files in os.listdir(programmes_dir_path)]
    programme_paths = [programmes_dir_path / programmes_files
                       for programmes_files in os.listdir(programmes_dir_path)]
    candidats = [Candidat(programme_path)
                 for programme_path in programme_paths]
    return candidats


def split_selection_candidats(string, candidats):
    """
    Split the input string into a list of candidats' nicknames, return the list.
    Return whether the input is valid.
    Input string : e.g. 'ma-me-ro'
    Input candidats = list of Candidat objects.
    """
    candidats_nicknames = [candidat.nickname for candidat in candidats]
    if len(string) == 0:
        valid_input = True
        return valid_input, candidats_nicknames
    else:
        valid_input = True
        selected_nicknames = string.lower().split('-')
        # Check that all nicknames are registered
        for selected_nickname in selected_nicknames:
            valid_input &= (selected_nickname in candidats_nicknames)
        return valid_input, selected_nicknames


def input_float(prompt, lb=-5, ub=5):
    """
    Input a float number in str format.
    Empty float results in 0.
    """
    string = input(prompt)
    if len(string) == 0:
        return 0.
    else:
        return max(min(float(string), ub), lb)

def input_boolean(script):
    yes_or_no = input(script).lower()
    if yes_or_no == 'y' or yes_or_no == 'yes' or yes_or_no == 'o' or yes_or_no == 'oui':
        yes_or_no = True
    elif yes_or_no == 'n' or yes_or_no == 'no' or yes_or_no == 'non':
        yes_or_no = False
    else:
        yes_or_no = True

def save_object_into_json(item, output_path):
    with open(output_path, 'w', encoding='utf8') as json_file:
        json.dump(item, json_file, ensure_ascii=False, indent=4)
    return


def save_results_bar_plot(name, score_by_candidate, write_path, show_graph):
    labels = list(score_by_candidate.keys())
    values = list(score_by_candidate.values())
    x = np.arange(len(labels))
    plt.figure(figsize=(14, 10))
    plt.bar(x, values, width=0.5, label='Scores',
            color='midnightblue', tick_label=labels)
    plt.hlines(y=0, xmin=-1/2, xmax=len(x)-1/2,
               colors='r', linestyles='dashed')
    plt.xticks(rotation=20)
    plt.grid()
    plt.ylim(bottom=-1.1, top=1.1)
    plt.xlim(left=-1/2, right=len(x)-1/2)
    plt.title(
        f"Score d'aligement politique de {name} avec les mesures principales de chaque candidat ??valu??. 1 = accord parfait, -1 = d??saccord parfait")
    plt.savefig(write_path)
    if show_graph:
        plt.show()


def main(programmes_dir=Path('candidats/'), output_dir=Path('resultats/')):
    """
    Main script, ask the selection of candidates, ask the questions and print results.
    """
    programmes_dir=Path(programmes_dir)
    output_dir=Path(output_dir)

    # Load candidates' profiles
    candidats = load_candidats(programmes_dir)

    # Intro
    print("---------------------------------------- Candidats 2022  ----------------------------------------\n")
    print("                        Bienvenue dans cette aide ?? la d??cision politique. \n")
    print("Vous devrez attribuer une note ?? chaque mesure des candidats choisis :")
    print("-5 = compl??tement en d??saccord, ... , 0 = Indiff??rent , ... , 5 : compl??tement d'accord")
    print("\n")

    name = input("Votre pr??nom : ")

    # Check if there already are results
    output_path = output_dir / (name+'.json')
    output_path_png = output_dir / (name+'.png')

    if output_path.exists():
        reuse_input = input_boolean("Des r??sultats ?? ce nom ont ??t?? trouv??s, les compl??ter ? (Si 'N', les r??sultats pr??c??dents seront ??cras??s) [Y/N] : ")
    else:
        reuse_input = False

    # Candidates selection
    print("\n")
    print("Veuillez choisir les candidats desquels vous voulez juger les propositions,")
    print("sous la forme d'une cha??ne de caract??res des diminutifs des candidats, s??par??s par '-'.")
    print("\n")

    print("Exemple : 'ma-me-ro' pour Macron, M??enchon, Roussel).")
    print("Pour juger les programmes de tous les candidats, appuyez sur Entr??e.")
    if reuse_input:
        print("Si vous notez ?? nouveau un candidat, son score pr??c??dent sera ??cras??.")
    print("\n")

    names_and_nicknames = [
        f"{candidat.name} : {candidat.nickname}" for candidat in candidats]
    prompt = '\n'.join(names_and_nicknames)
    print(f"Diminutif des candidats :\n{prompt}\n")

    valid_input = False
    while not valid_input:
        selection_candidats = input("Choix des candidats : ")
        valid_input, selected_candidats_nicknames = split_selection_candidats(
            selection_candidats, candidats)
        if not valid_input:
            print("S??lection incorrecte, veuillez r??essayer.")

    # Filter the candidats list based on selection
    selected_candidats = [
        candidat for candidat in candidats if candidat.nickname in selected_candidats_nicknames]

    selected_names = [f"{candidat.name}" for candidat in selected_candidats]
    prompt = '\n'.join(selected_names)
    print(f"Les candidats choisis sont :\n{prompt}\n")

    input("Appuyer sur Entr??e pour commencer.\n")

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
        score_by_candidate = json.load(
            open(output_path, "rb"), encoding="utf-8")
        # Re-initialize the scores of the selected candidates
        for candidat in selected_candidats:
            score_by_candidate[candidat.name] = 0.
    else:
        score_by_candidate = {
            candidat.name: 0. for candidat in selected_candidats}

    # Ask the questions
    for proposition in tqdm(proposition_keys, desc="Progression"):
        print("--------------------------------------------------------------------------------------------------")
        print(proposition)
        print("\n")
        candidate_name = propositions_dico[proposition]
        accord = input_float(
            "Accord avec la mesure (pas du tout d'accord : -5 , ... , 5 : compl??tement d'accord) : ", lb=-5, ub=5)
        score = float(accord)/5
        score_by_candidate[candidate_name] += score
        print("\n")

    print("\n---------------------------------------- C'est termin?? !  ----------------------------------------\n")
    input("Appuyez sur Entr??e pour voir vos r??sultats.")

    # Print results
    print("\n---------------------------------- R??sultats ----------------------------------\n")
    prompt = ', '.join(selected_names)
    print(f"Les candidats qui ont ??t?? not??s sont : {prompt}.")
    print(
        f"Voici les scores de {name} par candidats (compl??tement en d??saccord : -1 , ... , 1 : compl??tement en accord) :\n")

    # Average out each score
    for candidat in selected_candidats:
        score_by_candidate[candidat.name] /= candidat.num_propositions

    # Print the results in descending order
    sorted_scores = list(score_by_candidate.items())
    sorted_scores.sort(reverse=True, key=lambda x: x[1])
    for name_score in sorted_scores:
        candidate_name, score = name_score
        print(f"{candidate_name} : {round(score,2)}")
    print("\n")

    # Save the results in a json file
    save_object_into_json(score_by_candidate, output_path)
    print(f"R??sultats sauvegard??s ?? : {output_path_png}\n")
    show_graph = input_boolean("Montrer les r??sultats ? [Y/N]")
    save_results_bar_plot(name, score_by_candidate, output_path_png, show_graph)


    return


if __name__ == '__main__':
    fire.Fire(main)
