# IMS-map-for-benzenoids

Pour commencer, il est nécessaire d'avoir une structure de benzenoid qui a déjà subis un calcul d'optimisation.


Première étape : BeforeCalc

1) Placer le fichier .log ou .xyz de la molécule dans le dossier "input" de BeforeCalc

2) Lancer le programme BeforeCalc.py (!!! tous les fichiers présents dans le dossier "output" seront supprimer à l'exécution de BeforeCalc.py !!!)

3) Après l'exécution de BeforeCalc.py, les résultats se trouve dans le dossier "output", pour 1 fichier dans "input" plusieurs fichiers sont créé dans "output" (les fichiers conservent le nom du fichier d'origine) :
- U_name_file.com : Le fichier avec les points placer pour le calcul d'IMS
- R_name_file.com : créé en plus si molécule de multiplicité 1, similaire à "U_..." pour les points du calcul d'IMS mais paramètre de calcul changer
- name_file_Bonds.dat : Fichier possédant des informations nécessaire pour la génération des cartes lors de la deuxième étape, il faut le déplacer dans le dossier "input" de AfterCalc.

- name_file_rota.xyz : utiliser par le programme, inutile pour l'utilisateur 
- name_file.mdl : utiliser par le programme, inutile pour l'utilisateur 

4) Lancer en calcul les fichiers U_name_file.com et R_name_file.com avec Gaussian, quand les calculs sont finis passer à la deuxième étape.


Deuxième étape : AfterCalc

1) Placer les U_name_file.log et R_name_file.log des calculs terminer (ainsi que les name_file_Bonds.dat obtenue précédemment si cela n'a pas encore était fait) dans le dossier "input" de AfterCalc

2) Lancer le programme AfterCalc.py (!!! tous les fichiers présents dans le dossier "output" seront supprimer a l'exécution de AfterCalc.py !!!) 

3) Après l'exécution de AfterCalc.py, les résultats se trouve dans le dossier "output", pour chaque fichier U_... ou R_... dans "input" plusieurs fichiers sont créés dans "output" (les fichiers conservent le nom du fichier d'origine) :
- U_(or R_)name_file.dat : les données lier au .gnu du même nom pour crée la carte
- U_(or R_)name_file.gnu : les paramètre de traitement des données lier au .dat du même nom pour créer la carte
- U_(or R_)name_file.txt : Contient les données nécessaire à la reproduction de la carte avec d'autre outils

4) Ouvrir un terminal de commande linux dans le dossier "output" et lancer la commande "gnuplot U_(or R_)name_file.gnu" ou lancer gnuplot sur tous les fichiers .gnu, cela va fabriquer les cartes de tous les différents fichiers



