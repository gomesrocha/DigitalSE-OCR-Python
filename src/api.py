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

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return "<h1> API de teste </h1>"

@app.route('/', methods=['POST'])
def data_extract():
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

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()
