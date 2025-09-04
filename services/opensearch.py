

# from transformers import AutoTokenizer, AutoModel
from utils.embedder import get_embedding
from opensearchpy import OpenSearch

import json


def index_clauses(json_obj,contract_id):
    # with open(json_path, "r", encoding="utf-8") as f:
    #     clauses = json.load(f)
    try:
        client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "StrongPassw0rd!"),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False
        )

        index_name = "clauses_index"

        if not client.indices.exists(index=index_name):
            client.indices.create(
                index=index_name,
                body={
                    "settings": {"index": {"knn": True}},
                    "mappings": {
                        "properties": {
                            "clause_heading": {"type": "text"},
                            "contract_id": {"type": "keyword"},
                            "clause_id": {"type": "keyword"},
                            "clause": {"type": "text"},
                            "embedding": {"type": "knn_vector", "dimension": 384}
                        }
                    }
                }
            )
        print("the clause entering")
        json_response=[]
        for clause in json_obj["clauses"]:
            embedding = get_embedding(clause["clause"])
            doc_id=f"{contract_id}_{clause['clause_id']}"
            doc = {
                "clause_heading": clause.get("clause_heading", ""),
                "contract_id": contract_id,
                "clause_id": clause.get("clause_id", ""),
                "clause": clause["clause"],
                "embedding": embedding
            }

            client.index(index=index_name, id=doc_id, body=doc)
            doc = {
                "clause_heading": clause.get("clause_heading", ""),
                "clause_id": clause.get("clause_id", ""),
                "clause": clause["clause"],
            }
            json_response.append(doc)
        return json_response

    except Exception as e:
        raise RuntimeError(f"the runtime error:{str(e)}")
    


def search_clauses(query_text,top_k=10):
    # print(f"in search_clause def :{query_text},filter_text:{filter_text}, and filter_text2:{filter_text2}")
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "StrongPassw0rd!"),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False
    )

    query_embedding = get_embedding(query_text)
    search_query = {
            "size": top_k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_embedding,
                        "k": top_k
                    }
                }
            }
        }


    response = client.search(index="clauses_index", body=search_query)
    json_obj=[]
    print("🔍 Search Results:")
    for hit in response["hits"]["hits"]:
        data={
            "Score":hit['_score'],
            "contract_id":hit['_source']['contract_id'],
            "clause_id":hit['_source']['clause_id'],
            "contract heading":hit['_source']['clause_heading'],
            "clause":hit['_source']['clause'],
        }

        json_obj.append(data)
    return json_obj




