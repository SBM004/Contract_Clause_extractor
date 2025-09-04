# from connection import cursor,conn
from utils.connection import conn
import json
import os
import uuid
import datetime
from init_db import init_db
from flask import jsonify
init_db()
# conn.close()
def store_database(json_file,contract_id,file_name):
   
    # if json_path=="":
    #     return "invalid_path"
    # # cursor=conn.cursor()
    try:
        print("in database")
        print(type(json_file))
        cursor=conn.cursor()
        # print("type of contract")
        print(json_file.get("contract_type"))
        user_id="1" #for now took static then we can take the user_id from cookie
        cursor.execute("""
        INSERT INTO contracts (user_id,contract_id,contract_name,contract_type )  VALUES (%s,%s,%s,%s)

        """,(
            user_id,
            contract_id,
            file_name,
            json_file["contract_type"]

        ))
        conn.commit()
        print(cursor.rowcount)
        for clause in json_file["clauses"]:
            clause_id = str(uuid.uuid4())
            clause["clause_id"]=clause_id
            cursor.execute("""
                INSERT INTO clauses ( contract_id, clause_id, clause_heading, clause) values (
                %s,%s,%s,%s
                )
            """,(
                contract_id,
                clause_id,
                clause["clause_heading"],
                clause["clause"]))
        conn.commit()
        print(cursor.rowcount)
        
        print("saved in database")
        conn.close()
        return json_file
    except Exception as e:
        # Catch all unexpected errors
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)  
        }), 500 

# store("clause//123456.json")