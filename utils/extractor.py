

from services.llm import answer
from flask import jsonify, Response
from utils.tiktoken import estimate_token
import os
import fitz 
def extractor(file,file_id):
# def extractor()->str:
    try:
        print('in def')
        text=""
        pdf_bytes=file.read()
        # file_path="D:/python_venv/ClauseExtracter/PDFS/Non Disclosure Agreement.pdf"
        # file_path="D:/python_venv/ClauseExtracter/PDFS/annex-2-sample-non-disclosure-agreement.pdf"
        # file_path="D:/python_venv/ClauseExtracter/PDFS/NON_DISCLOSURE_AGREEMENT.pdf"

        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page_num in range(len(doc)):
                page=doc[page_num]
                text+=page.get_text("text")
        
        token_length=estimate_token(text)
        print(token_length)
        if token_length>100000:
            return {"error":"the pdf is too large"}
        response=answer(text,file_id,token_length)
        return response
        # return path
    except Exception as e:
        raise RuntimeError(f"Extractor failed: {str(e)}")


# extractor()
    