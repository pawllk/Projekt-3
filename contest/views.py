from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.forms import inlineformset_factory 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Player
from .models import Tournament
from .models import Participants
from .forms import CreateUserForm
from .forms import CreateContestForm
from .filter import ContestFilter

# Create your views here.
def start_page(request):
    tournaments = Tournament.objects.all()
    count = tournaments.count()
    pending = tournaments.filter(status="PENDING").count()
    tournaments_started = tournaments.filter(status="STARTED")
    started = tournaments_started.count()
    filter = ContestFilter(request.GET, queryset=tournaments)
    tournaments = filter.qs
    filter_started = ContestFilter(request.GET, queryset=tournaments_started)
    tournaments_started = filter.qs
    context = {'tournaments' : tournaments , 'started' : started, 'pending' : pending, 
               'tournaments_started' : tournaments_started, 'count' : count, 'filter' : filter}
    
    if request.user.is_authenticated:
        return render(request, 'user.html', context) 
    else:
        return render(request, 'guest.html', context)    
    

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
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)

# Logout view
def logout_page(request):
    logout(request)
    return redirect('login_page')

# User profile view  
def profile_page(request):
    if request.user.is_authenticated:
        user = request.user
        player = Player.objects.get(name=request.user)
        tournaments = player.tournament_set.all()
        count_arraving = tournaments.filter(status="PENDING").count()
        count_all = tournaments.count()
        filter = ContestFilter(request.GET, queryset=tournaments)
        tournaments = filter.qs
        context = {'user' : user, 'player' : player, 'tournaments' : tournaments, 
                   'count_all' : count_all, 'count_arraving' : count_arraving,
                   'filter' : filter}
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
                for i in range(int(contest.get_slots())):
                    Participants.objects.create(tournament=contest)
                return redirect('profile_page')
            
        context = {'form':form}
        return render(request, 'contest_creator.html', context)
    
    else:
        return redirect('login_page')
    
# Tournament updater view
@login_required(login_url='login')
def contestupdate_page(request, pk):
    tournament = Tournament.objects.get(id=pk)
    form = CreateContestForm(instance=tournament)
    if tournament.get_status() == 'STARTED':
        return redirect('profile_page')
    else:
        if request.method == 'POST':
            form = CreateContestForm(request.POST, instance=tournament)
            
            if form.is_valid():
                form.save()
                return redirect('profile_page')
        
        context = {'form' : form}
        return render(request, 'contest_creator.html', context)

# Tournament delet view
@login_required(login_url='login')
def contestdelete_page(request, pk):
    tournament = Tournament.objects.get(id=pk)
    if tournament.get_status() == 'STARTED':
        return redirect('profile_page')
    else:
        if request.method == 'POST':
            tournament.delete()
            return redirect('profile_page')
    
        context={'tournament' : tournament}
        return render(request, 'delete.html', context)
    
# Tournament app view
@login_required(login_url='login')
def add_page(request, pk):
    AddPageFormSet = inlineformset_factory(Tournament, Participants,fields=('tournament','player'), extra=0)
    tournament = Tournament.objects.get(id=pk)
    players = tournament.participants_set.all()
    form = AddPageFormSet(queryset=players, instance=tournament)
    if request.method == 'POST':
        form = AddPageFormSet(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    context={'formset' : form}
    return render(request, 'add_player.html', context)