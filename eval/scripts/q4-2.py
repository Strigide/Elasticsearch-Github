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

question_number = "4-2"

query = {
# Moyenne, médiane et stats avancées du champ "Rating" :
      "size": 0,
    "aggs": {
        "mean":{
            "avg":{
                "field": "Rating"
            }
        },
        "median":{
            "percentiles": {
              "field": "Rating",
              "percents": [50]
            }
        },
        "extended_stats": {
            "extended_stats": {
                "field": "Rating"
      }
    }
  }
}

response = client.search(index="eval", **query)

results = {}

results["4-2"] = dict(client.search(index="eval", **query))


with open("./eval/q_4-2_response.json", "w") as f:
    json.dump(results, f, indent=2)
