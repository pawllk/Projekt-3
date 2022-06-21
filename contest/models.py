from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, verbose_name="Name", null=True)
    date = models.DateField(auto_now_add=False, null=True)
    
    def __str__(self) -> str:
        return f"{(self.id-1)}-{self.name}"
    
class Tournament(models.Model):
    SLOTS = (
        ('2','2'),
        ('4','4'),
        ('6','6'),
        ('8','8'),
        ('10','10')
    )
    
    STATUS = (
        ('STARTED','STARTED'),
        ('PENDING','PENDING'),
        ('ENDED','ENDED')
    )
    
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=TRUE)
    name = models.CharField(max_length=200, verbose_name="Name", null=True)
    date = models.DateField(auto_now_add=False, null=True)
    time = models.TimeField(auto_now_add=False, null=True)
    slots = models.CharField(max_length=200, verbose_name="Slots", choices=SLOTS, null=True)
    status = models.CharField(max_length=200, verbose_name="Status", choices=STATUS, null=True)