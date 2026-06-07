from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
    ca_certs="./ca/ca.crt"
)

client.indices.put_mapping(
    index="eval",
    body={
        "properties": {
            "Review Text": {
                "type": "text",
                "fielddata": True
            }
        }
    }
)

print("Fielddata activé !")