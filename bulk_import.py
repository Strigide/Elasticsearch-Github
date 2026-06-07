from elasticsearch import Elasticsearch
import csv
from dotenv import load_dotenv
import os

load_dotenv()

client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
    ca_certs="./ca/ca.crt"
)

with open("Womens_Clothing.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    from elasticsearch import helpers
    helpers.bulk(client, reader, index="eval")
