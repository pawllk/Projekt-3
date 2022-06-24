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
    
    PHASE = (
        ('STARTING LADDER','STARTING LADDER'),
        ('SEMIFINAL','SEMIFINAL'),
        ('FINAL','FINAL')
    )
    
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, verbose_name="Name", null=True)
    date = models.DateField(auto_now_add=False, null=True)
    time = models.TimeField(auto_now_add=False, null=True)
    slots = models.CharField(max_length=200, verbose_name="Slots", choices=SLOTS, null=True)
    status = models.CharField(max_length=200, verbose_name="Status", choices=STATUS, default="PENDING")
    phase = models.CharField(max_length=200, verbose_name="Faza", choices=PHASE, default="STARTING LADDER")
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def get_slots(self) -> str:
        return self.slots
     
    def get_status(self) -> str:
        return f"{self.status}"
    
class Participants(models.Model):
    tournament = models.ForeignKey(to=Tournament, on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(to=Player, on_delete=models.DO_NOTHING, null=True)