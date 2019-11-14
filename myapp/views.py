from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import logout as do_logout, authenticate, login as do_login
from .forms import LoginForm, FilterForm, DetailForm
from .models import Estate, City, RentDate, Reservation, Service
from datetime import datetime
from decimal import *
from django.db.models import Count


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
    form = FilterForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            estates = Estate.objects.filter(
                city=request.POST['city']
            ).filter(
                rentdate__date__gte=request.POST['dateFrom'], 
                rentdate__date__lte=request.POST['dateTo'],
                rentdate__reservation__isnull=True,
                pax__lte=request.POST['pax']
            ).distinct()
 
            return render(request, 'myapp/home.html', {'estates': estates})
        else:
            return render(request, 'myapp/filter.html', {'form': form})
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
        rents_per_reservation = []
        reservations = Reservation.objects.filter(
            rentdate__estate__owner__id= request.user.id
        ).distinct()
        for r in reservations:
            rents = RentDate.objects.filter(reservation=r.id) #array de fechas de alquiler con id de reserva
            rents_per_reservation.append(rents)#array de array
        return render(request, 'myapp/reservations.html',{'rents_per_reservation': rents_per_reservation})
    return redirect('/admin')


def detail(request, id=0):   
    form = DetailForm(id)
    if request.method == "GET":
        estate = Estate.objects.get(id=id)
        services = Service.objects.filter(estate=id)
        return render(request,'myapp/product_detail.html', {'estate':estate, 'form':form, 'services':services})  
    return redirect('/')

def thanks(request, id=0):
    if request.method == "POST":
        
        form = DetailForm(data=request.POST, estateId=id)
        # if form.is_valid():
            # dates = form.cleaned_data['date']
            # form.is_valid method don't work.
            # return redirect('/')
        cod = datetime.today().strftime('%y-%m-%d-%H-%M-%S') + "-" + str(id) + "-" + str(request.user.id)
        prop = Estate.objects.get(id=id)
        getcontext().prec = 10
        total = (prop.dailyRate * form['date'].value().__len__()) * Decimal(1.08)
        user = form['user'].value()

        r = Reservation(code=cod, user=user, total=total)
        r.save()
        
        for i in form['date'].value():
            dte = int(i)
            rd = RentDate.objects.get(id=dte)
            rd.reservation = r
            rd.save()
        finalDates = RentDate.objects.filter(reservation=r.id)
        return render(request,'myapp/thanks.html', {'form':form, 'estate':prop, 'reservation':r, 'dates':finalDates, 'total':round(r.total, 2)},)  
    return redirect('/')

