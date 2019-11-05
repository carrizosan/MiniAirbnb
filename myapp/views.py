from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request,'myapp/index.html')

def login(request):
    return render(request,'myapp/login.html')

def signup(request):
    return render(request,'myapp/signup.html')
