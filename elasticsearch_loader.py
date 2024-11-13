from elasticsearch import Elasticsearch, helpers
import ndjson
import argparse
import uuid

# Initialize Elasticsearch
es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "Zac3QMwS3=qFQ-iXKJj1"), verify_certs=False)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--index')

args = parser.parse_args()

index = args.index
file = args.file

# Use ndjson to load NDJSON file
with open(file, 'r', encoding='utf-8') as json_file:
    json_docs = ndjson.load(json_file)  # Correctly loads NDJSON format

def bulk_json_data(json_list, _index):
    for doc in json_list:
        yield {
            "_index": _index,
            "_id": uuid.uuid4(),  # Unique ID for each document
            "_source": doc
        }

try:
    # Make the bulk call to Elasticsearch
    response = helpers.bulk(es, bulk_json_data(json_docs, index))
    print("\nRESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)
