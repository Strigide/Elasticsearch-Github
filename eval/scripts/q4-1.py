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

question_number = "4-1"

query = {
# Histogramme du champ "age" avec un interval de 20 :
  "size": 0,
    "aggs": {
      "price_distribution": {
        "histogram": {
          "field": "Age",
          "interval": 20,
          "min_doc_count": 0
      }
    }
  }
}

response = client.search(index="eval", **query)

results = {}

results["4-1"] = dict(client.search(index="eval", **query))


with open("./eval/q_4-1_response.json", "w") as f:
    json.dump(results, f, indent=2)
