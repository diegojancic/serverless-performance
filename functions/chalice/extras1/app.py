from chalice import Chalice, Response

app = Chalice(app_name='chalice-extras1')


@app.route('/')
def index():
	resp = "<html><body><h1>Hello World!</h1></body></html>"
	return Response(body=resp,
					status_code=200,
					headers={'Content-Type': 'text/html'})

