from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from myapp.models import RentDate, City, Estate
from datetime import date
from django.forms import widgets


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
    DATE_INPUT_FORMATS = ['%Y-%m-%d']
    pax = forms.IntegerField(label="Cantidad de Pax", min_value=1, max_value=10)
    dateFrom = forms.DateField(label="Desde", input_formats=DATE_INPUT_FORMATS)
    dateTo = forms.DateField(label="Hasta", input_formats=DATE_INPUT_FORMATS)

    class Meta:
        model = Estate
        fields = ['city']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()

