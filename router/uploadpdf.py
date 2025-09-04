

from flask import Flask, Blueprint, request, Response, jsonify
import os
import uuid
from utils.extractor import extractor
from database import store_database
from services.opensearch import index_clauses
import json

file_path = 'PDFS'

# Make sure upload folder exists
os.makedirs(file_path, exist_ok=True)

uploadR = Blueprint("uploadR", __name__)

@uploadR.route('/', methods=['GET', 'POST'])
def uploading():
    try:
        if request.method == 'POST':
            print(request.files)

            if "file" not in request.files:
                return Response("No file part", status=400)

            file = request.files["file"]
            if file.filename == "":
                return Response("No selected file", status=400)

            if not file.filename.endswith(".pdf"):
                return Response("Invalid file type. Only PDFs allowed.", status=400)

            

            file_id = str(uuid.uuid4())
            result = extractor(file, file_id) 
            if "error" in result:
                return jsonify({"error": "Processing Error", "details": result.get("error")}), 400
           
            result=store_database(result,file_id,file.filename)
            responses=index_clauses(result,file_id)
            
            
            # response={"contract_id":file_id,"responses":responses}
            # os.remove(path)
            # response=json.loads(responses)
            return jsonify(responses),200
            
            
            # return Response(
            #     f"File uploaded successfully! in open search and Database",
            #     status=200
            # )
        else:
            
            return Response("hello upload")

    except RuntimeError as re:  
        return jsonify({"error": "Processing Error", "details": str(re)}), 400

    except Exception as e:  
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    
