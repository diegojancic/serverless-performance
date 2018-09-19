from chalice import Chalice, Response

app = Chalice(app_name='website')


@app.route('/')
def index():
	resp = "<html><body><h1>Hello World!</h1></body></html>"
	return Response(body=resp,
					status_code=200,
					headers={'Content-Type': 'text/html'})


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
