# from transformers import AutoTokenizer,AutoModel
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import os
# import json
# from opensearchpy import OpenSearch





# def embedder():
#     tokenizer=AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


#     model=AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
#     with open("clause/123456.json", "r",encoding="utf-8") as f:
#         clauses = json.load(f)

#     # 2. Connect to OpenSearch
#     client = OpenSearch(
#         hosts=[{"host": "localhost", "port": 9200}],
#         http_auth=("admin", "StrongPassw0rd!"),  # if security enabled
#         use_ssl=True,
#         verify_certs=False,   # 🚨 skip self-signed cert check
#         ssl_show_warn=False 
#     )

# # 3. Load embedding model (example: MiniLM)
# # model = SentenceTransformer("all-MiniLM-L6-v2")

# # 4. Create index if not exists
#     index_name = "clauses_index"

#     if not client.indices.exists(index=index_name):
#         client.indices.create(
#             index=index_name,
#             body={
#                 "settings": {
#                    "index": {
#                         "knn": True   # enable k-NN search
#                     }   
#                 },
#                 "mappings": {
#                     "properties": {
#                         "clause_type":{"type":"text"},
#                         "clause_heading": {"type": "text"},
#                         "contract_id": {"type": "keyword"},
#                         "clause_id": {"type": "keyword"},
#                         "clause": {"type": "text"},
#                         "embedding": {"type": "knn_vector", "dimension": 384}
#                     }
#                 }
#             }
#         )
#     # clauses=json.load(json_path)
#     for clause in clauses:
#          #Insert clauses with embeddings

#         embedding = model.encoder(clause["clause"]).tolist()
#         doc = {
#             "clause_heading": clause["clause_heading"],
#             "contract_id": clause["contract_id"],
#             "clause_id": clause["clause_id"],
#             "clause": clause["clause"],
#             "embedding": embedding
#         }
#         client.index(index=index_name, body=doc)




from transformers import AutoTokenizer, AutoModel

import torch

def get_embedding(text):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
    return embedding


# def embedder_store():
#     # 1. Load tokenizer and model
#     tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
#     model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

#     # 2. Load clauses from JSON
#     with open("clause/123456.json", "r", encoding="utf-8") as f:
#         clauses = json.load(f)

#     # 3. Connect to OpenSearch
#     client = OpenSearch(
#         hosts=[{"host": "localhost", "port": 9200}],
#         http_auth=("admin", "StrongPassw0rd!"),
#         use_ssl=True,
#         verify_certs=False,
#         ssl_show_warn=False
#     )

#     index_name = "clauses_index"

#     # 4. Create index if not exists
#     if not client.indices.exists(index=index_name):
#         client.indices.create(
#             index=index_name,
#             body={
#                 "settings": {"index": {"knn": True}},
#                 "mappings": {
#                     "properties": {
#                         "clause_type": {"type": "text"},
#                         "clause_heading": {"type": "text"},
#                         "contract_id": {"type": "keyword"},
#                         "clause_id": {"type": "keyword"},
#                         "clause": {"type": "text"},
#                         "embedding": {"type": "knn_vector", "dimension": 384}
#                     }
#                 }
#             }
#         )

#     # 5. Insert clauses with embeddings
#     for clause in clauses:
#         # Tokenize text
#         inputs = tokenizer(clause["clause"], return_tensors="pt", truncation=True, padding=True)

#         # Get model outputs
#         with torch.no_grad():
#             outputs = model(**inputs)

#         # Mean Pooling over token embeddings to get a sentence embedding
#         embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

#         doc = {
#             "clause_heading": clause.get("clause_heading", ""),
#             "contract_id": clause.get("contract_id", ""),
#             "clause_id": clause.get("clause_id", ""),
#             "clause": clause["clause"],
#             "embedding": embeddings
#         }

#         client.index(index=index_name, body=doc)



# def embedder_search():
#     # 1. Load tokenizer and model
#     tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
#     model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

#     # 2. Load clauses from JSON
#     with open("clause/123456.json", "r", encoding="utf-8") as f:
#         clauses = json.load(f)

#     # 3. Connect to OpenSearch
#     client = OpenSearch(
#         hosts=[{"host": "localhost", "port": 9200}],
#         http_auth=("admin", "StrongPassw0rd!"),
#         use_ssl=True,
#         verify_certs=False,
#         ssl_show_warn=False
#     )

#     index_name = "clauses_index"

#     # 4. Create index if not exists
#     if not client.indices.exists(index=index_name):
#         client.indices.create(
#             index=index_name,
#             body={
#                 "settings": {"index": {"knn": True}},
#                 "mappings": {
#                     "properties": {
#                         "clause_type": {"type": "text"},
#                         "clause_heading": {"type": "text"},
#                         "contract_id": {"type": "keyword"},
#                         "clause_id": {"type": "keyword"},
#                         "clause": {"type": "text"},
#                         "embedding": {"type": "knn_vector", "dimension": 384}
#                     }
#                 }
#             }
#         )

#     # 5. Insert clauses with embeddings
#     for clause in clauses:
#         # Tokenize text
#         inputs = tokenizer(clause["clause"], return_tensors="pt", truncation=True, padding=True)

#         # Get model outputs
#         with torch.no_grad():
#             outputs = model(**inputs)

#         # Mean Pooling over token embeddings to get a sentence embedding
#         embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

#         doc = {
#             "clause_heading": clause.get("clause_heading", ""),
#             "contract_id": clause.get("contract_id", ""),
#             "clause_id": clause.get("clause_id", ""),
#             "clause": clause["clause"],
#             "embedding": embeddings
#         }

#         client.index(index=index_name, body=doc)
# embedder()