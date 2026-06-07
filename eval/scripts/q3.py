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

question_number = "3"

query = {
# Y'a-t-il des valeurs NULL dans les documents ? Avec l'exemple du champ Title.keyword :
  "query": {
    "term": {
      "Title.keyword": ""
    }
  }
}

results = {}

results["3"] = dict(client.search(index="eval", **query))


with open("./eval/q_3_response.json", "w") as f:
    json.dump(results, f, indent=2)

