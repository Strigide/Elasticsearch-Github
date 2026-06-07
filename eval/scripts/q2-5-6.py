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

question_number = "2-5-6"

query5 = {
# Combien d'articles du champ "Departement Name" appartient à sa division ("Division Name") :
  "size": 0,
  "aggs": {
    "by_division": {
      "terms": {
        "field": "Division Name"
      },
      "aggs": {
        "by_department": {
          "terms": {
            "field": "Department Name"
          }
        }
      }
    }
  }
}

query6 = {
# Combien d'articles uniques par Departement Name :
  "size": 0,
  "aggs": {
    "by_department": {
      "terms": {
        "field": "Department Name",
        "order": {
          "unique_products": "desc"
        }
      },
      "aggs": {
        "unique_products": {
          "cardinality": {
            "field": "Clothing ID"
          }
        }
      }
    }
  }
}


results = {}

results["2-5"] = dict(client.search(index="eval", **query5))
results["2-6"] = dict(client.search(index="eval", **query6))
with open("./eval/q_2_5-6_response.json", "w") as f:
    json.dump(results, f, indent=2, default=str)