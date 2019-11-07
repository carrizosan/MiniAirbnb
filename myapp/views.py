from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout as do_logout, authenticate, login as do_login
from .forms import SignUpForm, LoginForm
from .models import Estate


def index(request):
    if request.user.is_authenticated:
        estates = Estate.objects.all()
        return render(request, 'myapp/index.html',{'estates':estates})
    return redirect('/login')


def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect('/')
    return render(request, 'myapp/login.html', {'form': form})


def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user= form.save()
            if user is not None:
                do_login(request,user)
                return redirect('/')
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    return render(request,'myapp/register.html',{'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def reservations(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/reservations.html')
    return redirect('/login')


def detail(request, id=0):    
    if request.user.is_authenticated:
        estate = Estate.objects.get(id=id)
        return render(request,'myapp/product_detail.html', {'estate':estate})
    return redirect('/login')

