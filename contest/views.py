from multiprocessing import context
from unicodedata import name
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from .models import Player
from .models import Tournament
from .forms import CreateUserForm
from .forms import CreateContestForm

# Create your views here.
def start_page(request):
    tournaments = Tournament.objects.all()
    context = {'tournaments': tournaments}
    return render(request, 'dashboard.html', context)

# Register view
def register_page(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    
    else:
        form = CreateUserForm()
        
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                date = form.cleaned_data.get('date')
                Player.objects.create(
                    user=user,
                    name=username, 
                    date=date)
                messages.success(request, 'Account was created for ' + username)
                return redirect('login_page')
            
        context = {'form':form}
        return render(request, 'register.html', context)

# Login view
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
                return redirect('profile_page')
            else:
                messages.info('request', 'Username or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)

# Logout view
def logout_page(request):
    logout(request)
    return redirect('login_page')

# User profile view  
def profile_page(request, pk):
    if request.user.is_authenticated:
        user = request.user
        player = Player.objects.get(id=pk)
        context = {'user' : user, 'player' : player}
        return render(request, 'profile.html', context)
    else:
        return redirect('login_page')

# Tournament generator view
def contestcreator_page(request):
    if request.user.is_authenticated:
        form = CreateContestForm()
        
        if request.method == 'POST':
            form = CreateContestForm(request.POST)
            
            if form.is_valid():
                contest = form.save()
                player = Player.objects.get(name=request.user)
                contest.player = player
                contest.save()
                return redirect('start_page')
            
        context = {'form':form}
        return render(request, 'contest_creator.html', context)
    
    else:
        return redirect('login_page')