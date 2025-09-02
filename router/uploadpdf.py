# from flask import Flask, Blueprint, request, Response
# import os
# # from file import File
# import uuid
# file_path='PDFS'

# uploadR=Blueprint("uploadR",__name__)

# @uploadR.route('/',method=['POST'])
# def uploads():
#     file=request.files
#     id=uuid.uuid4()
#     file_name=id+'.pdf'
#     temp_file=os.path.join(file_path,file_name)
#     with  open(temp_file,"wb") as f:
#         f.write()


# from flask import Flask, Blueprint, request, Response,jsonify
# import os
# import uuid
# from extractor import extractor
# from database import store_database
# from opensearch import index_clauses
# file_path = 'PDFS'

# # Make sure upload folder exists
# os.makedirs(file_path, exist_ok=True)

# uploadR = Blueprint("uploadR", __name__)

# @uploadR.route('/', methods=['GET','POST'])
# def uploading():
#     if request.method == 'POST':
#         print(request.files)
#         if "file" not in request.files:
#             return Response("No file part", status=400)

#         file = request.files["file"]
#         if file.filename == "":
#             return Response("No selected file", status=400)

#         if not file.filename.endswith(".pdf"):
#             return Response("Invalid file type. Only PDFs allowed.", status=400)
#         try:
#             # Generate unique filename
#             file_id = str(uuid.uuid4())
#             file_name = file_id + ".pdf"
#             temp_file = os.path.join(file_path, file_name)

#             # Saving file and storing clauses in the database extracted from database
#             file.save(temp_file)
#             path=extractor(temp_file,file_id) #for now fiding path of the json
#             os.remove(temp_file)
#             store_database(path)
#             index_clauses(path)
#             os.remove(path)
#             return Response(f"File uploaded successfully! ID: {file_id} and json file path:{path}", status=200)
#         except Exception as e:
#         # Catch all unexpected errors
#             return jsonify({
#                 "error": "Internal Server Error",
#                 "details": str(e)  # 👈 remove in production for security
#             }), 500 
#     else:
#         return Response(f"hello upload")


from flask import Flask, Blueprint, request, Response, jsonify
import os
import uuid
from extractor import extractor
from database import store_database
from opensearch import index_clauses

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
            file_name = file_id + ".pdf"
            temp_file = os.path.join(file_path, file_name)
            file.save(temp_file)
            result = extractor(temp_file, file_id)
            if isinstance(result, tuple):
                path = result[0]  
            else:
                path = result
            os.remove(temp_file)
            store_database(path)
            index_clauses(path)

            os.remove(path)

            return Response(
                f"File uploaded successfully! in open search and Database",
                status=200
            )
        else:
            return Response("hello upload")

    except RuntimeError as re:  
        return jsonify({"error": "Processing Error", "details": str(re)}), 400

    except Exception as e:  
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    
