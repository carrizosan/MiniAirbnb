from django.contrib import admin
from .models import Owner,Estate,Reservation,RentDate

admin.site.register(Owner)
admin.site.register(Estate)
admin.site.register(Reservation)
admin.site.register(RentDate)
