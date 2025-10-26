from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser 
# Create your models here.
"""
class Basemodel(models.Model):
    
    id = models.UUIDField(primary_key=True , default=uuid4 , editable=False)
    
    class Meta:
        abstract = True 
        
"""     
        
class User(AbstractUser):
    
    class Role(models.TextChoices):
        GUEST = "GUEST" , "GUEST"
        HOST = "HOST" , "HOST"
        ADMIN = "ADMIN" , "ADMIN"
        
        
    id = models.UUIDField(primary_key=True , default=uuid4 , editable=False)
    #first_name = models.CharField(max_length=50 , blank=False)
    #last_name = models.CharField(max_length=50 , blank=False)
    #email = models.EmailField(unique=True , max_length=100 , blank=False)
    phone_number = models.CharField(max_length=25 , blank=True)
    role = models.CharField(choices= Role.choices , max_length=10) 
    #password = models.CharField(max_length=200 , blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
class Message(models.Model):
    message_id = models.UUIDField(editable=False , primary_key=True , default=uuid4)
    sender_id = models.ForeignKey(User , related_name="messsages" , on_delete=models.CASCADE)
    message_body = models.TextField(blank=False , max_length=5000)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    
class Conversation(models.Model) :
    conversation_id = models.UUIDField(primary_key=True , default=uuid4 , editable=False)
    participants_id = models.ManyToManyField(User , related_name="conversations" )
   
    created_at = models.DateTimeField(auto_now_add= True)
    