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

question_number = "2-1-4"

query1 = {
# Combien de Division Name uniques :
  "size": 0,
  "aggs": {
    "unique_makes": {
      "cardinality": {
        "field": "Division Name"
      }
    }
  }
}

query2 = {
# Combien de Department Name uniques :
  "size": 0,
  "aggs": {
    "unique_makes": {
      "cardinality": {
        "field": "Department Name"
      }
    }
  }
}

query3 = {
# Combien de Class Name uniques :
  "size": 0,
  "aggs": {
    "unique_makes": {
      "cardinality": {
        "field": "Class Name"
      }
    }
  }
}

query4 = {
# Combien d'articles uniques
  "size": 0,
  "aggs": {
    "cardinality": {
      "cardinality": {
        "field": "Clothing ID"
      }
    }
  }
}


results = {}

results["2-1"] = dict(client.search(index="eval", **query1))
results["2-2"] = dict(client.search(index="eval", **query2))
results["2-3"] = dict(client.search(index="eval", **query3))
results["2-4"] = dict(client.search(index="eval", **query4))

with open("./eval/q_2_1-4_response.json", "w") as f:
    json.dump(results, f, indent=2)

