from elasticsearch import Elasticsearch, exceptions
from dotenv import load_dotenv
import os, sys
load_dotenv()

es_api_key = os.environ['ES_API_KEY']
es = Elasticsearch("https://es01:9200",ca_certs="/config/ca/ca.crt",basic_auth=("elastic","elastic"))
#es = Elasticsearch("https://es01:9200",ca_certs="/config/ca/ca.crt",api_key=es_api_key)
print(es.info())

search_index = sys.argv[1]
query = sys.argv[2]

print(f'質問文：{query}')
print("キーワード検索のみ")

# キーワード検索のみ
query_body = {
   "query": {
      "match": {
         "description": query
      }
   }
}

result = es.search(index=search_index, body=query_body)
items = result['hits']['hits']
for i, item in enumerate(items):
   print(i+1,item['_source']['description'])
print("")

# キーワード検索＋Semantic Rerank
print("キーワード検索＋Semantic Rerank")
query_body = {
       "retriever": {
      "text_similarity_reranker": {
         "retriever": {
            "standard": {
               "query": {
                  "match": {
                     "description": query
                  }
               }
            }
         },
         "field": "description",
         "inference_id": "my-rerank",
         "inference_text": query,
         "rank_window_size": 10
#         "min_score": 0.5
      }
   }
}

result = es.search(index=search_index, body=query_body)
items = result['hits']['hits']
for item in items:
   print(item['_rank'],item['_score'],item['_source']['description'])
