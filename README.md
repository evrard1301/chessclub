
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

---
## Tutoriel

### Créer un joueur
Choisir ``[j] Nouveau joueur`` puis saisir son nom de famille,
son prénom, sa date de naissance au format jj/mm/aaaa, son genre et enfin son rang. 

### Créer un tournoi
Choisir ``[t] Nouveau tournoi``.

1. Choisir ``[i] Saisir informations`` et saisir le nom du tournoi, le lieu où il se déroule et à quelle date au format jj/mm/aaaa. Choisir ensuite le type de partie parmi bullet, blitz et rapide. Saisir la description du tournoi.

2. Choisir ``[j] Ajouter un joueur``, saisir son identifiant (consultable via la liste des joueurs: ``[l] Liste des joueurs``). Il doit y avoir huit joueurs par tournoi.

3. Choisir ``[r] Ajouter un tour``, saisir la date de début et de fin au format jj/mm/aaaa.

4. Enfin, choisir ``[t] Créer`` pour finaliser la création du tournoi.

### Simuler un tournoi
Choisir ``[J] Jouer un tournoi`` puis ``[c] Choisir un tournoi``. Choisir ensuite ``[j] Jouer``.

Pour chaque tour, saisir ``0`` si le premier joueur est gagnant, ``1`` si le second remporte le match ou bien ``2`` dans le cas d'un match nul.

À la fin du tournoi une liste des scores des joueurs est affichée.

### Mettre à jour le classement
Choisir ``[c] Éditer le classement`` puis ``[m] Mettre à jour le classement``.

### Afficher un rapport
Choisir ``[R] Rapports`` puis en fonction du rapport désiré:

* ``[a] Acteurs (par nom)``,
* ``[A] Acteurs (par classement)``,
* ``[t] Tournoi (acteurs par nom)``,
* ``[T] Tournoi (acteurs par classement)``,
* ``[l] Liste des tournois``,
* ``[L] Liste des tours``,
* ``[m] Liste des matchs``.


### Sauvegarder et charger

Pour sauvegarder, saisir ``[S] Sauvegarder``.
Pour charger, saisir ``[C] Charger``.