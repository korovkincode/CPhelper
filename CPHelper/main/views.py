from django.shortcuts import render

def index(request):
	return render(request, "main/index.html")

def signup(request):
	print('there')