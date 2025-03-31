from flask import Flask,request,jsonify
import requests

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello"

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()