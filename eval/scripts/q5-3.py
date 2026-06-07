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

question_number = "5-3"

query = {
# Les ID produits avec le plus de recommandations sont mis en avant, avec leur note moyenne respective :
  "size": 0,
  "aggs": {
    "by_product": {
      "terms": {
        "field": "Clothing ID",
        "size": 10,
        "order": {
          "total_recommendations": "desc"
        }
      },
      "aggs": {
        "avg_rating": {
          "avg": {
            "field": "Rating"
          }
        },
        "total_recommendations": {
          "sum": {
            "field": "Recommended IND"
          }
        }
      }
    }
  }
}

response = client.search(index="eval", **query)

results = {}

results["5-3"] = dict(client.search(index="eval", **query))


with open("./eval/q_5-3_response.json", "w") as f:
  json.dump(results, f, indent=2, default=str)
