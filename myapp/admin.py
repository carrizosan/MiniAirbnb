from django.contrib import admin
from .models import Owner,Estate,RentDate,City,Service

admin.site.register(Owner)
admin.site.register(City)
admin.site.register(Service)

class EstateAdmin(admin.ModelAdmin):
        list_display= ('title','owner','dailyRate','pax','city')
        search_fields = ('title', 'owner__username')
admin.site.register(Estate,EstateAdmin)

class RentDateAdmin(admin.ModelAdmin):
        fields = ['estate', 'date']
        list_display = ('date', 'estate')
        search_fields = ('date','estate__title')
admin.site.register(RentDate,RentDateAdmin)