from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
	resp = "<html><body><h1>Hello World!</h1></body></html>"
	return resp

    