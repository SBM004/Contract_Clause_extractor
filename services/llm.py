from google import genai
from flask import jsonify
from openai import OpenAI
# import google.generativeai as genai
# from google.genai import types
from dotenv import load_dotenv
from utils.prompts import prompts
# from prompts import prompt2
from utils.chunking import chunking
from services.opensearch import search_clauses
import json
# import file
load_dotenv()
import os


# genai.configure(os.environ['GOOGLE_API_KEY'])

client_gemini=genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
client_openai=OpenAI(api_key=os.environ["OPENAI_API_KEY"])



def answer(pdf_text:str,contract_id:str,token_length):
    temp_file='clause'
    
    try:
        # i have done this for gemini as its max_output_token is 8k
        # if(token_length<=2000):
        #     max_output_t=4000
        # elif token_length<6000:
        #     max_output_t=7000
        # else:
        #     max_output_t=8018
        
        #done this for openai as output token is 4k
        # if(token_length<=1000):
        #     max_output_t=2000
        # else:
        #     max_output_t=4000

        #condition for gemini
        if token_length<8018:
        #consition for openai    
        # if max_output_t!=4000:    
            prompt1=prompts(pdf_text,contract_id)
            response=client_gemini.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt1,
                # max_output_tokens= max_output_t
                config={
                "max_output_tokens": 8018,
                "temperature": 0.3,
                "top_p": 0.9,
                "top_k": 40
                }
            )
            print(response)
            raw_text=response.text.strip()

            ### for openai
            # response = client_openai.chat.completions.create(
            #     model="gpt-4o-mini",
            #     messages=[{"role": "user", "content": prompt1}],
            #     max_tokens=max_output_t,
            #     temperature=0.3,
            #     top_p=0.9
            # )
            # print(response)
            # raw_text = response.choices[0].message.content.strip()

            print(raw_text)
            if raw_text.startswith('```'):
                raw_text=raw_text.split('```')[1]
                raw_text = raw_text.lstrip("json").strip()
            json_file=json.loads(raw_text)
        else:
            chunks=chunking(pdf_text)
            json_file={"contract_type":None,"clauses":[]}
            for chunk in chunks:
                prompt1=prompts(chunk,contract_id)
                response=client_gemini.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt1,
                    # max_output_tokens= max_output_t
                    config={
                    "max_output_tokens": 8018,
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "top_k": 40
                    }
                )
                raw_text=response.text.strip()


                ##for openai
                ### for openai
                # response = client_openai.chat.completions.create(
                #     model="gpt-4o-mini",
                #     messages=[{"role": "user", "content": prompt1}],
                #     max_tokens=max_output_t,
                #     temperature=0.3,
                #     top_p=0.9
                # )
                # print(response)
                # raw_text = response.choices[0].message.content.strip()


                # print(raw_text)
                if raw_text.startswith('```'):
                    raw_text=raw_text.split('```')[1]
                    raw_text = raw_text.lstrip("json").strip()
                test_json_file=json.loads(raw_text)
                if not json_file["contract_type"]:
                    json_file["contract_type"]=test_json_file["contract_type"]
                    json_file["clauses"].extend(test_json_file["clauses"])
                else:
                    json_file["clauses"].extend(test_json_file["clauses"])
        # print(json.dumps(json_file, indent=2, ensure_ascii=False))
        print("here in try")
        return json_file
    except Exception as e:
        # Catch all unexpected errors
      raise RuntimeError(f"Extractor failed: {str(e)}")
   

def searching(clause:str):
    # temp_file='clause'  
    try:
        responses=search_clauses(clause)
    except Exception as e:
        # Catch all unexpected errors
      raise RuntimeError(f"Extractor failed: {str(e)}")
    
    # print(responses)
    return responses