# Elasticsearch - Analyse d'avis clients e-commerce

## Description
Ce repository a pour objectif de présenter des compétences sur la stack ELK (Elasticsearch, Logstash, Kibana).



## Prérequis
- Docker Desktop
- Python 3.x

## Installation

### 1. Cloner le repo
```bash
git clone <url-du-repo>
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
- `eval/` : requêtes et réponses Elasticsearch
- `bulk_import.py` : import du dataset
- `docker-compose.yml` : configuration du cluster