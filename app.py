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

from flask import Flask
from flask import jsonify
from flask import request
# and import Jamie's prediction model code here!

# Create an instance of Flask
app = Flask(__name__)

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

# Placeholder!
def choose_next_notes(note_codes):
   return [n+5 for n in note_codes]

# A COUPLE NOTES ON PYTHON AND FLASK:
# @app.route('/nextnote') is a function decorator, which modifies the function
# defined below it.

# Example:

# @app.route('/nextnote')
# def hello():
#   return "Hello world"

# This tells Flask to run the hello() function whenever the client requests
# the URL of the app ending with /nextnote (example: localhost/nextnote).
# Then Flask takes the return value of hello() and sends it to the client
# as its response, so the client will receive "Hello" as the response body!
