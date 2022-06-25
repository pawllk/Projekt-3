from cmath import phase
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, verbose_name="Name", null=True)
    date = models.DateField(auto_now_add=False, null=True)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
class Tournament(models.Model):
    SLOTS = (
        ('2','2'),
        ('4','4'),
        ('8','8'),
    )
    
    STATUS = (
        ('STARTED','STARTED'),
        ('PENDING','PENDING'),
        ('ENDED','ENDED')
    )
    
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, verbose_name="Name", null=True)
    date = models.DateField(auto_now_add=False, null=True)
    time = models.TimeField(auto_now_add=False, null=True)
    slots = models.CharField(max_length=200, verbose_name="Slots", choices=SLOTS, null=True)
    status = models.CharField(max_length=200, verbose_name="Status", choices=STATUS, default="PENDING")
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def get_slots(self) -> str:
        return self.slots
     
    def get_status(self) -> str:
        return f"{self.status}"
    
class Participants(models.Model):
    tournament = models.ForeignKey(to=Tournament, on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=True)
    
class Match(models.Model):
    
    PHASE = (
        ('FAZA I', 'FAZA I'),
        ('FAZA II', 'FAZA II'),
        ('FAZA III', 'FAZA III'),
    )
    
    tournament = models.ForeignKey(to=Tournament, on_delete=models.CASCADE, null=True)
    phase = models.CharField(max_length=200, choices=PHASE, default="FAZA I")
    a_player = models.CharField(max_length=200, null=True)
    b_player = models.CharField(max_length=200, null=True)
    
class Winner(models.Model):
    tournament = models.ForeignKey(to=Tournament, on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return f"{self.player.name}"