# from connection import cursor,conn
from connection import conn
import json
import os
from flask import jsonify
cursor=conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS clauses (
    contract_type VARCHAR(225) NOT NULL,
    contract_id   VARCHAR(225) NOT NULL,
    clause_id   INT NOT NULL,
    clause_heading VARCHAR(225),
    clause  TEXT,
    PRIMARY KEY (contract_id, clause_id)
)""")
# conn.close()
conn.commit()
def store_database(json_path:str):
    if json_path=="":
        return "invalid_path"
    # cursor=conn.cursor()
    try:
        with open(json_path,"r",encoding="utf-8") as f:
            json_data=json.load(f)
        
        for clause in json_data:
            cursor.execute("""
                INSERT INTO clauses (contract_type, contract_id, clause_id, clause_heading, clause) values (
                %s,%s,%s,%s,%s
                )
            """,(clause["contract_type"],
                clause["contract_id"],
                clause["clause_id"],
                clause["clause_heading"],
                clause["clause"]))
        conn.commit()
        print("saved in database")
        
        # os.remove(json_path)
        conn.close()
    except Exception as e:
        # Catch all unexpected errors
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)  
        }), 500 

# store("clause//123456.json")