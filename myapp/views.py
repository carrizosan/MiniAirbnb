from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import logout as do_logout, authenticate, login as do_login
from .forms import LoginForm, FilterForm, DetailForm
from .models import Estate, City, RentDate, Reservation
from datetime import datetime
from decimal import *


# def index(request):
#     if request.user.is_authenticated:
#         estates = Estate.objects.all()
#         return render(request, 'myapp/filter.html',{'estates':estates})
#     return redirect('/login')

def index(request):
    cities = City.objects.all()
    rentDates = RentDate.objects.all()
    form = FilterForm()
    return render(request, 'myapp/filter.html',{'cities':cities,'rentDates':rentDates, 'form':form})

def home(request):
    form = FilterForm()
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            estates = Estate.objects.filter(
                city=request.POST['city']
            ).filter(
                rentdate__date__gte=request.POST['dateFrom'], 
                rentdate__date__lte=request.POST['dateTo']
            ).distinct()
 
            return render(request, 'myapp/home.html', {'estates': estates})
        else:
            return redirect('/')
    else:
        return render(request, 'myapp/home.html')


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


# def register(request):
#     form = SignUpForm()
#     if request.method == "POST":
#         form = SignUpForm(data=request.POST)
#         if form.is_valid():
#             user= form.save()
#             if user is not None:
#                 do_login(request,user)
#                 return redirect('/')
#     form.fields['username'].help_text = None
#     form.fields['password1'].help_text = None
#     form.fields['password2'].help_text = None
#     return render(request,'myapp/register.html',{'form': form})

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
    form = DetailForm(id)
    if request.method == "GET":
        estate = Estate.objects.get(id=id)
        return render(request,'myapp/product_detail.html', {'estate':estate, 'form':form})
    elif request.method == "POST":
        form = DetailForm(data=request.POST, estateId=id)
        # if form.is_valid():
            # dates = form.cleaned_data['date']
            # form.is_valid method don't work.
            # return redirect('/')
        cod = datetime.today().strftime('%y-%m-%d-%H-%M-%S') + "-" + str(id) + "-" + str(request.user.id)
        prop = Estate.objects.get(id=id)
        getcontext().prec = 10
        total = (prop.dailyRate * form['date'].value().__len__()) * Decimal(1.08)

        r = Reservation(code=cod, user=request.user.id, total=total)
        r.save()

        for i in form['date'].value():
            dte = int(i)
            rd = RentDate.objects.get(id=dte)
            rd.reservation = r
            rd.save()
            return redirect('/')

