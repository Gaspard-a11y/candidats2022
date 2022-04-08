# Candidats 2022
Cet outil permet de chiffrer le taux d'adhésion de l'utilisateur aux mesures des différents candidats à l'éléction présidentielle française de 2022.

Une fois lancé, le script énonce 20 propositions anonymisées par candidats, qu'il faut noter de -5 (complètement de désaccord) à 5 (complètement d'accord) (0=indifférent).

## Démo en ligne

Une démo en ligne est rendue possible grâce à Google Colab, ici:

> https://colab.research.google.com/

Selectionner l'onglet 'GitHub' et rentrer l'adresse de ce repo :

> https://github.com/Gaspard-a11y/candidats2022

Ensuite, cliquer sur 'demo.ipynb' (confirmer l'ouverture) et suivre les instructions qui s'affichent.

## Installation locale

Il suffit de créer un environnement virtuel et d'y installer les packages nécessaires :
> pip install requirements.txt

Pour lancer le script :

> python main.py

TODO next: 
Generate a unique random seed from the name and save it
Save the answers instead of the scores, so that the questionnaire can be stopped and continued later
Add option to go back to a previous question -> counter instead of for loop?
add 'I don't know' prompt with '?'