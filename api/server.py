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
# and import Jamie's prediction model code here!

# Create an instance of Flask
app = Flask(__name__)

# When client makes a POST request to /nextnote route and provides a note,
# send back the next note as a response based on the prediction model
@app.route('/nextnote', methods=['POST'])
def send_next_note():
    return jsonify({'nextNote': choose_next_note(65)})

# Placeholder!
def choose_next_note(note_code):
   return 55 

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

