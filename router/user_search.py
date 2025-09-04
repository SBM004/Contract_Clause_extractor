from flask import Blueprint, Response, request, jsonify
import json
from services.llm import searching

Search=Blueprint("Search",__name__)

@Search.route('/',methods=['POST'])
def searches():
    body=request.get_json()
    responses=searching(body["clause"])
    
    # response=json.loads(responses)
    return jsonify(responses),200


