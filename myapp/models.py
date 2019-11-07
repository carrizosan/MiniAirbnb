from django.db import models
import datetime, os
from django.contrib.auth.models import User

class Owner(User):
    pass

    class Meta:
        verbose_name_plural = 'Propietarios'

######################################################

class City (models.Model):
    title = models.CharField(max_length=100)
        
    class Meta:
        verbose_name_plural='Ciudades'

    def __unicode__(self):
        return '{}'.format(self.title)



######################################################

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Estate (models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    dailyRate = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to=get_image_path,blank=True, null=False)
    city = models.ForeignKey(City,on_delete=models.PROTECT, null=False)
    descripcion = models.TextField(max_length=500)
    

    class Meta:
        verbose_name_plural='Propiedades'

    def __unicode__(self):
        return '{}'.format(self.title)

######################################################
class Reservation (models.Model):
    code = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        verbose_name_plural='Reservaciones'
        ordering=('total','code')

    def __unicode__(self):
        return '{}'.format(self.total)

######################################################
class RentDate(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT)
    estate = models.ForeignKey(Estate, on_delete=models.PROTECT, null=True)
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural='Fecha de Alquiler'
        ordering=('date','estate')

