import os

import fire

programmes_folder = '.\programmes'


def main(candidats='all'):
    # TODO allow selection of candidates
    print("---------- Candidats 2022  ----------")
    print("Bienvenue dans cette aide à la décision politique.")

    programme_paths = [os.path.join(programmes_folder, programmes_files)
                       for programmes_files in os.listdir(programmes_folder)]
    num_mesures = 0

    print("Le système va anonymement vous proposer 20 mesures par candidat, et pour chaque vous devrez attribuer deux notes:")
    print("mesure inutile : 0 - ... - 5 : mesure indispensable")
    print("pas du tout d'accord : 0 - ... - 5 : complètement d'accord")

    return


if __name__ == '__main__':
    fire.Fire(main)
