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

question_number = "5-1"

query = {
# A partir de l'histogramme de la question 4-1, déterminer les articles achetés par tranche d'âge :
  "size": 0,
  "aggs": {
    "age_histogram": {
      "histogram": {
        "field": "Age",
        "interval": 20
      },
      "aggs": {
        "by_class": {
          "terms": {
            "field": "Class Name"
          }
        }
      }
    }
  }
}

response = client.search(index="eval", **query)

results = {}

results["4-4"] = dict(client.search(index="eval", **query))


with open("./eval/q_4-4_response.json", "w") as f:
    json.dump(results, f, indent=2)
