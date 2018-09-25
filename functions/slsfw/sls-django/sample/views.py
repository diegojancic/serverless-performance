from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
	
	resp = "<html><body><h1>Hello World!</h1></body></html>"
	return HttpResponse(resp)
	