from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    events = models.ManyToManyField('Event', related_name='cities')
    venue = models.CharField(max_length=100, default="None")
    time = models.DateField(default=now)
    guidelines = models.TextField(default="None")
    image = models.ImageField(
        upload_to="image_uploads/city_pic/", default='ropar.png')

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('solo', 'Solo'),
        ('team', 'Team'),
    ]

    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='solo')
    min_participants = models.PositiveIntegerField(null=True, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(default= "none")

    def clean(self):
        if self.event_type == 'team':
            if self.min_participants is None or self.max_participants is None:
                raise ValidationError("Min and Max participants are required for team events.")
            
            if self.min_participants > self.max_participants:
                raise ValidationError("Min participants cannot be greater than Max participants.")
        
        elif self.event_type == 'solo':
            if self.min_participants or self.max_participants:
                raise ValidationError("Min and Max participants should be empty for solo events.")
    
    def __str__(self):
        return self.name


class Head(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    institute_name = models.CharField(max_length=200)
    year_of_passing = models.IntegerField()
    program_enrolled = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
 
    solo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.event.event_type == 'solo':
            self.solo = True
        else:
            self.solo = False

        super(Head, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name}"
    
class Team(models.Model):

    head = models.OneToOneField(Head, on_delete=models.CASCADE, related_name='team')
    team_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Team: {self.team_name} (Head: {self.head.name})"
    
class TeamMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_members')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    institute_name = models.CharField(max_length=200)
    year_of_passing = models.IntegerField()
    program_enrolled = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __str__(self):
        return f"{self.name} ({self.head.team.team_name} - {self.head.event.name})"

