from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from myapp.models import RentDate, City, Estate
from datetime import date
import datetime
from django.forms import widgets
from airbnb.settings import DATE_INPUT_FORMATS, PAX_QUANTITY_CHOICE
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import DateTimePickerInput

# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100, required=True)
#     last_name = forms.CharField(max_length=100, required=True)
#     email = forms.EmailField(required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User
#         # I've tried both of these 'fields' declaration, result is the same
#         # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
#         fields = UserCreationForm.Meta.fields + \
#             ('first_name', 'last_name', 'username',
#              'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    error_messages = {
    'invalid_login': _(
        "Usuario Inexistente"
    )} 

class FilterForm(forms.ModelForm):
    # YEARS = ['2019', '2020', '2021']
    # MONTHS = {
    #     1:_('ENE'), 2:_('FEB'), 3:_('MAR'), 4:_('ABR'),
    #     5:_('MAY'), 6:_('JUN'), 7:_('JUL'), 8:_('AGO'),
    #     9:_('SEP'), 10:_('OCT'), 11:_('NOV'), 12:_('DIC')
    # }

    pax = forms.ChoiceField(choices=PAX_QUANTITY_CHOICE, label="", help_text="Cantidad de pax")
    dateFrom = forms.DateField(label="", input_formats=DATE_INPUT_FORMATS,help_text="Desde",
                                widget=DateTimePickerInput(
                                    format='%Y-%m-%d',options={'minDate':(datetime.datetime.today().strftime("%Y-%m-%d"))}).start_of('event days'))
    dateTo = forms.DateField(label="", input_formats=DATE_INPUT_FORMATS, help_text="Hasta",
                                widget=DateTimePickerInput(format='%Y-%m-%d').end_of('event days'))
    # dateTo = forms.DateField(widget=forms.SelectDateWidget(years=YEARS, months=MONTHS))

    class Meta:
        model = Estate
        fields = ['city']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()
        self.fields['city'].label = ""
        self.fields['city'].help_text = "Ciudad"

    def clean(self):
        cleaned_data = super(FilterForm, self).clean()
        date1 = str(self.cleaned_data['dateFrom'])
        date2 = str(self.cleaned_data['dateTo'])
        
        if date1 and date2:
            if date1 > date2:
                raise forms.ValidationError(_('Combinación de fechas incorrecta'), code='invalid')
        return cleaned_data
        


class DetailForm(forms.ModelForm):
    user = forms.CharField(label="", max_length=30, help_text="Ingrese su nombre")
    email = forms.EmailField(label="", help_text="Ingrese su e-mail")

    class Meta:
        model = RentDate
        fields = ['date']
    
    def __init__(self, estateId, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.ModelMultipleChoiceField(
            queryset=RentDate.objects.filter(estate__id=estateId, reservation__isnull=True),
            label="Fechas disponibles:",
            help_text="Seleccione las fechas a reservar: CTRL+Click",
        )
        

    

