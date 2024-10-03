from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers
import argparse
from dotenv import load_dotenv
import os
load_dotenv()
import json

parser = argparse.ArgumentParser()
# required args
parser.add_argument('--index_name', dest='index_name',
                    required=False, default='esre')
parser.add_argument('--file', dest='file',
                    required=False, default='data.json')

args = parser.parse_args()

def data_generator(file_json, index, pipeline):
    for doc in file_json:
        yield {
            "_index": index,
            "_source": doc,
        }

es = Elasticsearch("https://es01:9200",ca_certs="/config/ca/ca.crt",basic_auth=("elastic", "elastic"))
#print(es.info())

print("Indexing documents, this might take a while...")
with open(args.file, 'r') as file:
    file_json = json.load(file)
total_documents = len(file_json)
progress_bar = tqdm(total=total_documents, unit="documents")
success_count = 0

for response in helpers.streaming_bulk(client=es, actions=data_generator(file_json, args.index_name, args.index_name)):
    if response[0]:
        success_count += 1
    progress_bar.update(1)
    progress_bar.set_postfix(success=success_count)

progress_bar.close()

# Calculate the success percentage
success_percentage = (success_count / total_documents) * 100
print(f"Indexing completed! Success percentage: {success_percentage}%")
print("Done indexing documents!")