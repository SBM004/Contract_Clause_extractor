

# from transformers import AutoTokenizer, AutoModel
from embedder import get_embedding
from opensearchpy import OpenSearch

import json


def index_clauses(json_path:str):
    with open(json_path, "r", encoding="utf-8") as f:
        clauses = json.load(f)

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
                        "contract_type": {"type": "keyword"},
                        "clause": {"type": "text"},
                        "embedding": {"type": "knn_vector", "dimension": 384}
                    }
                }
            }
        )
    print("the clause entering")
    for clause in clauses:
        embedding = get_embedding(clause["clause"])
        doc_id=f"{clause["contract_id"]}_{clause["clause_id"]}"
        doc = {
            "clause_heading": clause.get("clause_heading", ""),
            "contract_id": clause.get("contract_id", ""),
            "clause_id": clause.get("clause_id", ""),
            "clause": clause["clause"],
            "contract_type":clause["contract_type"],
            "embedding": embedding
        }
        client.index(index=index_name, id=doc_id, body=doc)

    print("Clauses indexed successfully!")


def search_clauses(query_text,filter_text="",filter_text2="",top_k=3):
    print(f"in search_clause def :{query_text},filter_text:{filter_text}, and filter_text2:{filter_text2}")
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "StrongPassw0rd!"),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False
    )

    query_embedding = get_embedding(query_text)
    filters = []
    if filter_text:   # contract_id
        filters.append({"term": {"contract_id": filter_text}})
    if filter_text2:  # contract_type
        filters.append({"term": {"contract_type.keyword": filter_text2}})
    print(filters)   
    if filters==[]:
        print("in 1st")
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
    elif filters and query_text:
        print("in 2nd")
        search_query = {
            "size": top_k,
            "query": {
                "bool": {
                    "filter":filters,
                    "must": {
                        "knn": {
                            "embedding": {
                                "vector": query_embedding,
                                "k": top_k
                            }
                        }
                    }
                }
            }
        }
    else:
        print("Filters only")
        search_query = {
            "size": top_k,
            "query": {
                "bool": {
                    "filter": filters
                }
            }
        }


    response = client.search(index="clauses_index", body=search_query)
    json_file=[]
    print("🔍 Search Results:")
    for hit in response["hits"]["hits"]:
        data={
            "Score":hit['_score'],
            "contract_id":hit['_source']['contract_id'],
            "clause_id":hit['_source']['clause_id'],
            "contract heading":hit['_source']['clause_heading'],
            "contract_type":hit['_source']['contract_type'],
            "clause":hit['_source']['clause'],
        }

        json_file.append(data)
        # print(f"Score: {hit['_score']:.4f}")
        # print(f"contract_id:{hit['_source']['contract_id']}")
        # print(f"Clause_id:{hit['_source']['clause_id']}")
        # print(f"contract heading:{hit['_source']['clause_heading']}")
        # # print(f"contract_:{hit['_source']['clause_id']}")
        # print(f"Clause: {hit['_source']['clause']}")
        # # print(f"")
        # print("-" * 50)

    # print (json_file,"\n\n")
    
    return json.dumps(json_file)

# index_clauses()
# search_clauses("Inclusion in Confidential Information, Confidential Information shall include any financial, business, proprietary")




