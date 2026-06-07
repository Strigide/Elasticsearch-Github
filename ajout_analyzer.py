from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
    ca_certs="./ca/ca.crt"
)

# Fermeture de l'index pour modifier les settings
client.indices.close(index="eval")

# Ajout de l'analyzer
client.indices.put_settings(
    index="eval",
    body={
        "analysis": {
            "analyzer": {
                "std_english": {
                    "type": "stop",
                    "stopwords": "_english_"
                }
            }
        }
    }
)

# Réouverture de l'index
client.indices.open(index="eval")

print("Analyzer ajouté avec succès !")