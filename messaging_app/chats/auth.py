from .models import User
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed



class CustomAPI(authentication.BaseAuthentication):
    
    
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return None
        
       
        
        try:
            prefix , key  = auth_header.split()
           
            
        except ValueError:
            raise AuthenticationFailed("Invalid Header")

        
        if  prefix.lower() != "token":
            return None
        
        try:
            user = User.objects.get(id = key)
        
        except ValueError:
            raise AuthenticationFailed("Invalid User Key")
        
        return (user , None)
    
    
    def authenticate_header(self, request):
        return "Token"
        
        