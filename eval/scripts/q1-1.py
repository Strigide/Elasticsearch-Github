from elasticsearch import Elasticsearch
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
    ca_certs="./ca/ca.crt"
)

#Pour obtenir le mapping de l'index "eval"
template = client.indices.get_mapping()

with open("./eval/index_template.json", "w") as f:
    json.dump(dict(template), f, indent=2)