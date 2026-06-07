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

question_number = "5-2"

query = {
# Les termes les plus utilisés pour les avis des produits à la note de 5/5 :
    "size": 0,
    "query": {
      "range":{
        "Rating":{
          "lt":2
        }
      }
    },
      "aggs": {
        "significant_text": {
          "significant_text": {
            "field": "Review Text"
        }
      }
    }
  }

response = client.search(index="eval", **query)

results = {}

results["5-2"] = dict(client.search(index="eval", **query))


with open("./eval/q_5-2_response.json", "w") as f:
    json.dump(results, f, indent=2)
