from django.db import models
import datetime
from django.contrib.auth.models import User

class Owner(User):
    pass

    class Meta:
        verbose_name_plural = 'Propietarios'

######################################################
class Estate (models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    dailyRate = models.DecimalField(max_digits=10,decimal_places=2)
    
    class Meta:
        verbose_name_plural='Propiedades'

    def __unicode__(self):
        return '{}'.format(self.title)

    


######################################################
class Reservation (models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.PROTECT)
    date = models.DateTimeField()
    code = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        verbose_name_plural='Reservaciones'
        ordering=('date','code')

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

######################################################

