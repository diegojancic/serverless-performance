from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
	resp = "<html><body><h1>Hello World from " + os.environ.get("STAGE", "<unknown location>") + "!</h1></body></html>"
	return resp
