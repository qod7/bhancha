from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request,'mainapp/index.html')

def login(request):
	return render(request,'mainapp/login.html')

def home(request):
	return render(request,'mainapp/home.html')

def signup(request):
	return render(request,'mainapp/signup.html')

