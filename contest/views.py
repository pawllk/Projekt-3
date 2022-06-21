from email import message
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages

from .forms import CreateUserForm
# Create your views here.
def start_page(request):
    return render(request, 'dashboard.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            key = request.POST.get('password')
            user = authenticate(request, username=name, password=key)
            
            if user is not None:
                login(request, user)
                return redirect('start_page')
            else:
                messages.info('request', 'Username or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)
    

def register_page(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                date = form.cleaned_data.get('date')
                print(date)
                messages.success(request, 'Account was created for ' + user)
                return redirect('login_page')
            
        context = {'form':form}
        return render(request, 'register.html', context)

def logout_page(request):
    logout(request)
    return redirect('login_page')