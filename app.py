################################################################################
# To test this from the client side once the server is running,
# open the app's homepage in your browser, copy-paste this code
# into the browser console, and press enter to run it:
'''
fetch('/nextnote', {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(65) // example for playing a single note
}).then(response => response.json()).then(console.log);
'''
################################################################################
from waitress import serve
from flask import Flask, jsonify, request
from api.midi import full_continued_sequence, gen_ngrams

import os

# Create an instance of Flask
app = Flask(__name__)

# generate ngrams on server start
ngram_dicts = gen_ngrams('api/midifiles/BeautyAndBeast.mid')

# Serve the app's home page  -- placeholder!
@app.route('/', methods=['GET'])
def homepage():
    return app.send_static_file('index.html')

# Serve the app's home page  -- placeholder!
@app.route('/stylesheet.css', methods=['GET'])
def stylesheet():
    return app.send_static_file('stylesheet.css')


# Serve the app's home page  -- placeholder!
@app.route('/script.js', methods=['GET'])
def script():
    return app.send_static_file('script.js')


# Serve the app's home page  -- placeholder!
@app.route('/piano.js', methods=['GET'])
def piano():
    return app.send_static_file('piano.js')

# When client makes a POST request to /nextnote route and provides a note,
# send back the next note as a response based on the prediction model
@app.route('/nextnote', methods=['POST'])
def send_next_note():
    return jsonify({'nextNotes': choose_next_notes(request.json)})

def choose_next_notes(note_codes):
   return full_continued_sequence(note_codes,5,ngram_dicts)


serve(app, host='0.0.0.0', port=os.environ.get('PORT'))
