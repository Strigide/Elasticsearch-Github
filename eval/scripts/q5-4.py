#! /usr/bin/python
from elasticsearch import Elasticsearch
import json
import warnings
from dotenv import load_dotenv
import os

load_dotenv()

warnings.filterwarnings("ignore")

# Connexion au cluster
client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
    ca_certs="./ca/ca.crt"
)

question_number = "5-4"

query = {
# 10 produits ayant au moins 20% des mots les plus utilisés dans les avis négatifs dans au moins 10 avis. Avec leur moyenne de note.
  "size": 0,
  "query": {
    "match": {
      "Review Text": {
        "query": "cheap disappointed terrible awful poor worst unflattering returned",
        "operator": "or",
        "minimum_should_match": "20%"
      }
    }
  },
  "aggs": {
    "by_product": {
      "terms": {
        "field": "Clothing ID",
        "size": 10,
        "min_doc_count": 10
      },
      "aggs": {
        "avg_rating": {
          "avg": {
            "field": "Rating"
          }
        }
      }
    }
  }
}

response = client.search(index="eval", **query)

results = {}

results["5-4"] = dict(client.search(index="eval", **query))


with open("./eval/q_5-4_response.json", "w") as f:
    json.dump(results, f, indent=2)
