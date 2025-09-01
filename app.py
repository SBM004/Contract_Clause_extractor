from flask import Flask , Response
from router.uploadpdf import uploadR
from router.user_search import Search
app=Flask(__name__)

app.register_blueprint(uploadR, url_prefix='/upload')
app.register_blueprint(Search, url_prefix='/search')
@app.route('/', methods=['GET'])
def p():
    return Response("hello world")
app.run(host='0.0.0.0', port=2000,debug=True)