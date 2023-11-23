from bottle import route, run, post, static_file, request, template
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import cv2
import numpy as np
import pytesseract
import json


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

    img_str = document.file.read()
    nparr = np.frombuffer(img_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detected_text: str = text_detection(img_np)
    translated_text: str = translatorFunc(detected_text, from_lang, to_lang)

    detected_text = detected_text

    data = {
        "detected_text": detected_text,
        "translated_text": translated_text
    }
    return json.dumps(data)
    

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def text_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    return text


model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", cache_dir="./cache").to("cuda")
def translatorFunc(sentence, fromLang, toLang):
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", cache_dir="./cache", src_lang=fromLang)
    model_inputs = tokenizer(sentence, return_tensors="pt")
    model_inputs.to("cuda")
    #the translation itself
    generated_tokens = model.generate(
        **model_inputs,
        forced_bos_token_id = tokenizer.lang_code_to_id[toLang]
    )

    translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    translated_text = str(translation).strip("[]''")

    return translated_text


run(host='localhost', port=8080)