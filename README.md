# Goal
Deploy the cross encoder on Elasticsearch Machine Learning Node, and execute Semantic Reranking based on the results of Lexical Search.

# Prerequite
You need more than 8GB RAM for Machine Learning.
If you choose smaller model, it may run with less RAM.

# Steps
1. Craete `.env`
```
STACK_VERSION = 8.15.2
ELASTIC_PASSWORD = elastic
KIBANA_PASSWORD = elastic
ES_PORT = 9200
CLUSTER_NAME = test
LICENSE = trial
MEM_LIMIT = 1610612736
ML_MEM_LIMIT = 8589934592
KIBANA_PORT = 5601
```
2. `docker compose up -d`
3. Upload Cross Encoder model to Machine Learning node
Japanese Cross Encoder model is used here. Change `--hub-model-id` accordingly.
```
docker exec -it semantic_reranking-eland-1 \
eland_import_hub_model \
--url https://es01:9200 \
-u elastic -p elastic \
--hub-model-id hotchpotch/japanese-reranker-cross-encoder-xsmall-v1 \
--task-type text_similarity \
--ca-certs /config/ca/ca.crt \
--start
```
4. Create Inference Endpoint
```
docker exec -it semantic_reranking-python-1 curl --cacert /config/ca/ca.crt -u elastic:elastic -X PUT "https://es01:9200/_inference/rerank/my-rerank" -H 'Content-Type: application/json' -d'
{
  "service": "elasticsearch",
  "service_settings": {
    "num_allocations": 1,
    "num_threads": 1,
    "model_id": "hotchpotch__japanese-reranker-cross-encoder-xsmall-v1" 
  }
}
'
```
5. Ingest data
This is Japanese language only.
```
docker exec -it semantic_reranking-python-1 python /src/ingest.py --index_name=rerank --file=/src/data.json
```
6. Search and Reranking
```
 docker exec -it semantic_reranking-python-1 python /src/rerank.py rerank 京都の観光名所を教えて
```
