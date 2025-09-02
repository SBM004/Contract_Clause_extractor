
def prompts(pdf_text:str,contract_id:str)->str:
    prompt1=f"""
    you are a legal assistant helping to extract the clauses from the contract and returning the result in json format with clause heading if they are under same heading clause number as per in the extracted pdf text, 
    each clause mush be in the form
    contract_type:<type of contract>
    clause_heading: <heading of the clause>
    contract_id: {contract_id}
    clause_id: <number of the clause as per PDF if it is null add clause_heading >
    clause:<clause_heading , text of the clause>
    Extract the clauses from the content given below
    
    content:
    {pdf_text}


    """

    return prompt1


def prompt2(prompt:str)->str:

    # prompt2=f"""
    # you are a smart legal assistant helping. user prompt mentions clauses and if user also mentions contract id get the information from prompt of user then returning  in json format given below :
    
    # text:<the clause types by user>
    # contract_id:<contract id mentioned by user>

    # if clause id is not mentioned then return the json format as
    
    
    # text:<the clause types by user>
    # contract_id:""
    
    # content:
    # {prompt}


    # """
    prompt2=f"""
   You are a smart legal assistant.  
Extract information from the user prompt.  

If the user mentions both clauses and a contract_id, return in this JSON format:


  "clause": <id the clause is mentioned by user> other wise empty string "" ,
  "contract_id": <contract id mentioned by user>,
  "contract_type":<if user mentions contract_type> other wise empty string " "


If the user mentions clauses but no contract_id, return:


  "clause": <id the clause is mentioned by user> other wise empty string "" ,
  "contract_id": "",
   "contract_type":<if user mentions contract_type> other wise empty string" "
  

content: {prompt}



Important rules:
- Return **only valid JSON**.
- Do not include code, explanations, markdown, or backticks.
- Do not write Python. Just output JSON.


    """
    return prompt2

