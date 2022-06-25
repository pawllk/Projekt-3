from django.contrib import admin
from .models import Player
from .models import Participants
from .models import Tournament
from .models import Match
from .models import Winner

# Register your models here.
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Participants)
admin.site.register(Match)
admin.site.register(Winner)