from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):

	date = forms.DateField(required=True)
 
	class Meta:
		model = User
		fields = ['username', 'email', 'date', 'password1', 'password2']