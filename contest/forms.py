from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Tournament
from .models import Participants

class CreateUserForm(UserCreationForm):
    
	date = forms.DateField(required=True)
 
	class Meta:
		model = User
		fields = ['username', 'email', 'date', 'password1', 'password2']
  
class ContestFilter(forms.ModelForm):
    
    class Meta:
        model = Tournament
        fields = '__all__'
  
class CreateContestForm(forms.ModelForm):
    
    class Meta:
        model = Tournament
        fields = ['name', 'date', 'time', 'slots', 'status']
        
class AddUserForm(forms.ModelForm):
    
    class Meta:
        model = Participants
        fields = ['tournament', 'player']