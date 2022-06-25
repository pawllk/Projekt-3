from multiprocessing import context
import random
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
from .models import Match
from .forms import CreateUserForm
from .forms import CreateContestForm
from .forms import StartContestForm
from .forms import AddResultForm
from .forms import EndContestForm
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
    if request.user.is_authenticated:
        context={'tournaments' : tournaments, 'filter' : filter,
                'count' : count, 'started' : started, 'pending' : pending}
        return render(request, 'user.html', context) 
    
    else:
        context={'tournaments_started' : tournaments_started,
                'started' : started, 'pending' : pending}
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
@login_required(login_url='login_page')
def contestupdate_page(request, pk):
    tournament = Tournament.objects.get(id=pk)
    form = CreateContestForm(instance=tournament)
    
    if tournament.get_status() == 'PENDING':
        if request.method == 'POST':
            form = CreateContestForm(request.POST, instance=tournament)
            
            if form.is_valid():
                form.save()
                return redirect('profile_page')
        
        context = {'form' : form}
        return render(request, 'contest_creator.html', context)
        
    else:
        return redirect('profile_page')
        

# Tournament delet view
@login_required(login_url='login_page')
def contestdelete_page(request, pk):
    tournament = Tournament.objects.get(id=pk)
    if request.method == 'POST':
        tournament.delete()
        return redirect('profile_page')
    
    context={'tournament' : tournament}
    return render(request, 'delete.html', context)
    
# Tournament add player view
@login_required(login_url='login_page')
def add_page(request, pk):
    tournament = Tournament.objects.get(id=pk)
    if tournament.status == "PENDING":
        AddPageFormSet = inlineformset_factory(Tournament, Participants,
                                           fields=('tournament','player'),
                                           extra=0,
                                           can_delete=False,
                                           )
        players = tournament.participants_set.all()
        form = AddPageFormSet(queryset=players, instance=tournament)
    
        if request.method == 'POST':
            form = AddPageFormSet(request.POST, instance=tournament)
            if form.is_valid():
                form.save()
                return redirect('profile_page')

        context={'formset' : form}
        return render(request, 'add_player.html', context)
    else:
        return redirect('profile_page')
        
   

# View of tournament view
def view_page(request, pk):
    tournament = Tournament.objects.get(id=pk)
    players = tournament.participants_set.all()
    games_first = tournament.match_set.all().filter(phase="FAZA I")
    games_second = tournament.match_set.all().filter(phase="FAZA II")
    games_third = tournament.match_set.all().filter(phase="FAZA III")
    winner = tournament.winner_set.all()
    count = players.count()
    matches = (count  - 1) 
    context = {'players' : players, 'count' : count, 'tournament' : tournament,
               'matches' : matches, 'games_first' : games_first,
               'games_second' : games_second, 'games_third' : games_third,
               'winner' : winner}
    
    return render(request, 'view.html', context)

# Start tournament view
@login_required(login_url='login_page')
def startcontest_page(request, pk):
    tournament = Tournament.objects.get(id=pk)
    players = tournament.participants_set.all()
    form = StartContestForm(instance=tournament)
    #creat list of names to draw for game lader
    draw = []
    for player in players:
        draw.append(player.player.name)
    random.shuffle(draw)
    
    if tournament.status == "PENDING":
        if request.method == 'POST':
            form = StartContestForm(request.POST, instance=tournament)
            if form.is_valid():
                form.save()
                for i in range(players.count()//2):
                    Match.objects.create(
                        tournament=tournament,
                        a_player=draw.pop(),
                        b_player=draw.pop()
                        )
                return redirect('profile_page')
            
        context = {'form' : form}
        return render(request, 'startcontest.html', context)

    else:
        return redirect('profile_page')
    
# Viev for adding new matches in next phase
@login_required(login_url='login_page')
def add_match(request, pk):
    tournament = Tournament.objects.get(id=pk)
    if tournament.status == "STARTED":
        games_first = tournament.match_set.all().filter(phase="FAZA I")
        games_second = tournament.match_set.all().filter(phase="FAZA II")
        games_third = tournament.match_set.all().filter(phase="FAZA III")
        form = AddResultForm()
        if request.method == 'POST':
            form = AddResultForm(request.POST)
            if form.is_valid():
                match = form.save()
                match.tournament = tournament
                match.save()
                return redirect('profile_page')
            
        context = {'form' : form, 'games_first' : games_first,
                'games_second' : games_second, 'games_third' : games_third}
        return render(request, 'match_creator.html', context)
    else:
        return redirect('profile_page')

@login_required(login_url='login_page')
def end_match(request, pk):
    tournament = Tournament.objects.get(id=pk)
    tournament = Tournament.objects.get(id=pk)
    if tournament.status == "STARTED":
        form = EndContestForm()
        if request.method == "POST":
            form = EndContestForm(request.POST)
            if form.is_valid():
                winner = form.save()
                winner.tournament = tournament
                winner.save()
                tournament.status = "ENDED"
                tournament.save()
                return redirect('profile_page')
            
        context = {'form' : form, 'tournament' : tournament}
        return render(request, 'end_match.html', context)

    else:
        return redirect('profile_page')