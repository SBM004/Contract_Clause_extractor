from flask import Blueprint, Response, request, jsonify
import json
from gemini import searching

Search=Blueprint("Search",__name__)

@Search.route('/',methods=['POST'])
def searches():
    body=request.get_json()
    responses=searching(body["prompt"])
    
    response=json.loads(responses)
    return jsonify(response),200


