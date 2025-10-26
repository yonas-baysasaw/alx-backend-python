from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
class IsParticipantOfConversation(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
       
        return obj.participants_id == request.user
    
    
class IsSenderOfMessage(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in ["PUT" ,"PATCH" ,"DELETE"]:
            return True
        
        return obj.sender_id == request.user
    