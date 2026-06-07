# Elasticsearch - Analyse d'avis clients e-commerce

## Description
Ce repository a pour objectif de présenter des compétences sur la stack ELK (Elasticsearch, Logstash, Kibana) dans un environnement de travail professionnel avec Docker.

Il présente une analyse d'un jeu de données composés de commentaires d'une boutique en ligne de vêtements, format CSV au travers de scripts python générant des json répondant à des questions.
Le dossier `eval/screenshots_kibana` permet d'accéder à des graphiques créés sur l'outil Dashboard de Kibana rendant la lecture des résultats plus claire et visuelle.
J'ai écrit mon raisonnement pour les questions statistiques subtiles à plusieurs réponses possibles.

Le jeu de données s'appelle "Womens_Clothing.csv" et est disponible dans les fichiers de ce repository.

Le cluster est configuré pour être sur 3 noeuds. L'index est sur 2 shards et 1 replica.

## Description du jeu de données

Le CSV "Womens_Clothing" est composé de 28227 lignes et 10 champs (colonnes). 

Les colonnes et leur mapping sont : Clothing ID (integer), Age (integer), Title (keyword - ignore_above:256), Review Text (text, keyword - ignore_above:256), Rating (integer), Recommended IND (integer), Positive Feedback Count (integer), Division Name (keyword), Department Name (keyword) et Class Name (keyword).


## Prérequis
- Docker Desktop
- Python 3

## Installation

### 1. Cloner le repo
```bash
git clone https://github.com/Strigide/Elasticsearch-Github
cd Elasticsearch-Github
```

### 2. Configurer l'environnement
```bash
cp .env.example .env
# Editer .env avec vos propres mots de passe
```

### 3. Lancer le cluster
```bash
sudo sysctl -w vm.max_map_count=262144
docker compose up -d
# Attendre que le cluster soit healthy (~2 minutes)
```

### 4. Copier le certificat SSL
```bash
docker cp elasticsearchgithub-es01-1:/usr/share/elasticsearch/config/certs/ca/ ./
```

### 5. Importer les données
```bash
pip install -r requirements.txt
python3 bulk_import.py
python3 ajout_analyzer.py
python3 setup_fielddata.py
```

## Accès
- Elasticsearch : https://localhost:9200
- Kibana : http://localhost:5601
- User : elastic

## Structure du projet
- `eval/` : requêtes et réponses Elasticsearch / data vizualisation Kibana.
Le dossier `eval/scripts` comprend les scripts python qui génère les json qui répondent aux questions. Les scripts `q_2-1-4.py` et `q_2-5.py` génèrent 2 json pour les questions 2.1 à 2.5.
Le dossier `eval/reponses` comprend les json générés par les scripts, avec à l'intérieur les réponses.
Le dossier `eval/screenshots_kibana` comprend les screenshots des réponses créées sur l'outil Kibana.
- `bulk_import.py` : import du dataset
- `docker-compose.yml` : configuration du cluster
- `ajout_analyzer.py` : initialise l'analyzer pour filtrer les stopwords en anglais.
- `setup_fielddata.py` : permet de faire des recherches par mot dans "Review Text" sur l'outil Dashboard de Kibana.

## Questions
Tout au long de ce repository, nous allons répondre aux questions suivantes :

2 - Établir les valeurs uniques:

    2-1 Établir le nombre de valeurs uniques pour le champ "Division Name"
    2-2 Établir le nombre de valeurs uniques pour le champ "Department Name"
    2-3 Établir le nombre de valeurs uniques pour le champ "Class Name"
    2-4 Combien d'articles sont disponibles dans le dataset ?

Établir les appartenances:

    2-5 Déterminer le nombre d'articles du champ "Department Name" appartenant à sa Division (champ "Division Name").
    2-6 Déterminer les articles uniques du champ "Department Name".


3 - Qualité des données.

    3- Vérifier l’existence ou non de valeurs nulles dans le jeu de données


4 - Établir les premières statistiques du jeu de données.

    4-1 Créer un histogramme du champ "age" avec une valeur d'intervalle à "20"
    4-2 Faire une analyse statistique des notes, déterminer la moyenne et la médiane parmi tous les produits présents dans le dataset
    4-3 Faire une agrégation des notes pour chaque classe de produit (Champ "Class Name")
    4-4 Avec votre histogramme "age", créer un bucket des produits "Class Name" et déterminer les articles les plus représentés selon l'âge des clients.


5 - Analyses avancées

    5-1 Quels sont les termes les plus présents parmi les articles les MIEUX notés ?
    5-2 Quels sont les termes les plus présents parmi les articles les MOINS bien notés ?
    5-3 Quels produits votre client devrait garder en priorité dans son catalogue ?
    5-4 À l'inverse, sur quels produits votre client NE devrait PAS investir ?


## Détails des réponses de la partie 5 :

La partie 5 - Analyses avancées propose deux questions avec plusieurs réponses possibles (5-3 et 5-4). Cette sous-partie me permettra d'expliquer mon raisonnement par question, avec un raisonnement et une exécution différente par question.

5-3 Quels produits votre client devrait garder en priorité dans son catalogue ?
Le CSV n'a pas de champ "Prix". En revanche, il a un champ "Recommended IND", qui est un booléen. J'ai donc considéré que les Clothing ID (articles uniques) ayant le plus de somme totale dans recommended IND (sum) pouvaient être les plus intéressants, car ils ont dû être achetés assez de fois ET être assez satisfaisant pour être les plus recommandés. Pour confirmer mon idée, j'ai ajouté la moyenne des notes (avg Ratings) à chaque article. Ce résultat tend à donner raison à mon raisonnement.

5-4 À l'inverse, sur quels produits votre client NE devrait PAS investir ?
Nous avons déterminé dans la question 5-2 des mots souvent utilisés dans les reviews des articles les moins biens notés.
Parmi ceux-ci : "cheap disappointed terrible awful poor worst unflattering returned".
Mon raisonnement a donc été de regarder les articles qui ont au moins 10 reviews avec au moins l'un de ces mots. J'ai également ajouté la moyenne des notes à chaque article.


## Quel screenshot correspond à quelle question ?

2-1 Établir le nombre de valeurs uniques pour le champ "Division Name"
`division_name_kibana.png`

2-2 Établir le nombre de valeurs uniques pour le champ "Department Name"
`dptm_name_kibana.png`

2-3 Établir le nombre de valeurs uniques pour le champ "Class Name"
`class_name_kibana.png`

2-4 Combien d'articles sont disponibles dans le dataset ?
`number_of_articles_kibana.png`

2-5 Déterminer le nombre d'articles du champ "Department Name" appartenant à sa Division (champ "Division Name").
`count_dptm_div_kibana.png`

2-6 Déterminer les articles uniques du champ "Department Name".
`unique_id_per_dptm.png`

4-1 Créer un histogramme du champ "age" avec une valeur d'intervalle à "20"
`age_interval_20_kibana.png`

4-2 Faire une analyse statistique des notes, déterminer la moyenne et la médiane parmi tous les produits présents dans le dataset
`avg_rating_id_kibana.png` et `median_rating_id_kibana.png`

4-4 Avec votre histogramme "age", créer un bucket des produits "Class Name" et déterminer les articles les plus représentés selon l'âge des clients.
`histo_age_classname_kibana.png`

5-1 Quels sont les termes les plus présents parmi les articles les MIEUX notés ?
`words_good_ratings.png`

5-3 Quels produits votre client devrait garder en priorité dans son catalogue ?
`recommanded_avg_rating.png`
(Dans ce graphique, un graphique en barre ET en ligne pour le nombre de recommandation par ID avec l'abscisse de gauche en indice + un graphique en ligne pour la moyenne des ratings par ID avec l'abscisse de droite en indice.)