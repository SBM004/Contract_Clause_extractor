from google import genai
from flask import jsonify
# import google.generativeai as genai
from dotenv import load_dotenv
from prompts import prompts, prompt2
# from prompts import prompt2
from opensearch import search_clauses
import json
# import file
load_dotenv()
import os


# genai.configure(os.environ['GOOGLE_API_KEY'])

client=genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

def answer(pdf_text:str,contract_id:str):
    temp_file='clause'
    prompt1=prompts(pdf_text,contract_id)
    response=client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt1
    )
    # path=os.path.join(temp_file,)
    # print(response.text)

    raw_text=response.text.strip()

    if raw_text.startswith('```'):
        raw_text=raw_text.split('```')[1]
        raw_text = raw_text.lstrip("json").strip()
    try:
        json_file=json.loads(raw_text)
        print("here in try")
        j='.json'
        print("here")
        path=os.path.join(temp_file,contract_id+j)
        with open(path,"w",encoding="utf-8") as f:
            json.dump(json_file,f,indent=2, ensure_ascii=False)
        
        return path
    except Exception as e:
        # Catch all unexpected errors
      raise RuntimeError(f"Extractor failed: {str(e)}")
   


def searching(pdf_text:str):
    # temp_file='clause'
    prompt=prompt2(pdf_text)
    response=client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )
    # path=os.path.join(temp_file,)
    print(response.text)

    raw_text=response.text.strip()

    if raw_text.startswith('```'):
        raw_text=raw_text.split('```')[1]
        raw_text = raw_text.lstrip("json").strip()
    try:
        json_file=json.loads(raw_text)
        print("here in try")
    except Exception as e:
        # Catch all unexpected errors
      raise RuntimeError(f"Extractor failed: {str(e)}")
    print(json_file)
    responses=search_clauses(json_file.get('clause'),json_file.get('contract_id'),json_file.get('contract_type'))
    # print(responses)
    return responses