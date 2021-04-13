import flask
from flask import request, jsonify, redirect, url_for, send_from_directory
import os
import pytesseract
import cv2
from timeit import default_timer as timer
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True
UPLOAD_FOLDER = "./"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return "<h1> OCR </h1>"

@app.route('/', methods=['POST'])
def data_extract():
    t = time.process_time()
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = cv2.imread(filename)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        options = ""
        text = pytesseract.image_to_string(rgb, config=options)
        
    elapsed_time = time.process_time() - t
    
    texto = "O tempo decorrido foi de {}".format(elapsed_time)
    return text

@app.route('/api/ocr', methods=['POST'])
def ocr_extract():
    t = time.process_time()
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = cv2.imread(filename)
        imageg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (i1, i2) = cv2.threshold(imageg, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        options = ""
        text = pytesseract.image_to_string(i2, config=options)
        
    elapsed_time = time.process_time() - t
    
    texto = "O tempo decorrido foi de {}".format(elapsed_time)
    return text

@app.route('/api/ocr2', methods=['POST'])
def ocr_extract2():
    t = time.process_time()
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = cv2.imread(filename)
        imageg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (i1, i2) = cv2.threshold(imageg, 200, 255, cv2.THRESH_BINARY)
        options = ""
        text = pytesseract.image_to_string(i2, config=options)
        
    elapsed_time = time.process_time() - t
    
    texto = "O tempo decorrido foi de {}".format(elapsed_time)
    return text 

app.run()
