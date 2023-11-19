from bottle import route, run, post, static_file, request
import cv2
import numpy as np

@route('/<filename>')
def serve_static(filename):
    return static_file(filename, root='static/')

@route('/')
def index():
    return serve_static('index.html')

@post('/translate')
def translate():
    document = request.files.get('document')
    from_lang = request.forms.get('from_lang')
    to_lang = request.forms.get('to_lang')
    printed_or_handwritten = request.forms.get('document_type')

    img_str = document.file.read()
    nparr = np.fromstring(img_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('static/translated.png', img_np)

    document.filename

run(host='localhost', port=8080)