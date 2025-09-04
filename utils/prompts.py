
def prompts(pdf_text:str,contract_id:str)->str:
    prompt1=f"""
    you are a legal assistant helping to extract the clauses from the contract and returning the result in json format with clause heading if they are under same heading clause number as per in the extracted pdf text, 
    each clause mush be in the form contract_type at start then list of clauses in the format given below
    {{
    "contract_type":"<type of contract = Non Disclosure Agreement or Master Service Agreement or Software License Agreement>",
    clauses:[
    {{
        
        
        "clause_heading": "<heading of the clause>"
        "clause":"<clause_heading , text of the clause>"
 

    }}
    ]
    }}


   
    Extract the clauses from the content given below
    
    content:
    {pdf_text}


    """

    return prompt1


#  {{
        
#         "contract_id": "{contract_id}"
#         "contract_type":"<type of contract>",
#         "clause_heading": "<heading of the clause>"
#         "clause":"<clause_heading , text of the clause>"
 

#     }}