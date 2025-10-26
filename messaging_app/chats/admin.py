from django.contrib import admin
from .models import *
# Register your models here.



class conversionadmin(admin.ModelAdmin):
    list_display = ["conversation_id" , "created_at"]
    
class Useradmin(admin.ModelAdmin):
    list_display = ["username" ,"role"]
    
    
    
admin.site.register(User , Useradmin)
admin.site.register(Conversation , conversionadmin)