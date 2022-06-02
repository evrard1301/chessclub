
# ChessClub
![chessclub logo](doc/slides/img/logo_club.png)

---
ChessClub est un programme console permettant de gérer des tournois d'échecs. Ce projet s'inscrit dans la formation [développeur d'application python](https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python) d'[openclassrooms](https://openclassrooms.com/fr/).


## Fonctionnalités
* Création de **joueurs**.
* Création de **tournois**.
* Simulation d'un tournoi.
* Génération des paires de joueurs selon l'**algorithme du système Suisse**.
* Affichage des **scores** après un tournoi.
* Mise à jour manuelle du **classement des joueurs**.
* Génération de **rapports**.
* Sauvegarde et chargement dans une **base de données** JSON.

## Installation
ChessClub dépend de:

* lxml,
* beautifulsoup,
* tinydb,
* pytest (pour les tests unitaires),
* behave (pour les tests d'acceptations).

Commandes d'installations:
```
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Usage
Après installation, la commande suivante permet d'exécuter le programme:

```
$ python main.py
```

Par défaut la base de données utilisée se nommera *db.json*.
Il est possible de changer cela avec les flags ``--db <nom_bdd>`` 
ou bien *via* la forme longue ``--database <nom_bdd>``.

```
$ python main.py --database hello.json
```

Enfin, une aide est disponible avec les flags ``-h`` et ``--help``.

```
$ python main.py --help
```

Il est possible de générer un rapport flake8 en utilisant flake8-html.

```
$ flake8 model view controller main.py --format html --htmldir flake8_html_report
```

Le script ``make_report.sh`` fait exactement cela.

```
$ chmod +x make_report.sh
$ ./make_report.sh
```
