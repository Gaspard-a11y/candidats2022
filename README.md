# Candidats 2022
Chiffrer le taux d'adhésion aux mesures des différents candidats à l'éléction présidentielle française de 2022.

20 propositions anonymisées par candidats à noter de -5 (complètement de désaccord) à 5 (complètement d'accord) (0=indifférent).

Pour installer cloner, créer un venv puis :
> pip install requirements.txt

Pour lancer le script, simplement :

> python main.py

TODO next: 
Generate a unique random seed from the name and save it
Save the answers instead of the scores, so that the questionnaire can be stopped and continued later
Add option to go back to a previous question -> counter instead of for loop?
add 'I don't know' prompt with '?'