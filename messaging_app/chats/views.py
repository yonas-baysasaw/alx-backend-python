from django.shortcuts import render
from rest_framework import viewsets , filters , status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .permissions import IsParticipantOfConversation , IsSenderOfMessage
from .filters import MessageFilter
from .pagination import LargeResultPagination

# Create your views here.


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConvsersationSerial
    name = "ConversationViewset"
    filter_backends = [filters.SearchFilter]
    search_fields =  ["particapant__first_name","participant__lanst_name"]
    parser_classes = [IsParticipantOfConversation , IsAuthenticated]
    filterset_class = [MessageFilter]
    
    
    def create(self, request, *args, **kwargs):
        
        serial = self.get_serializer(data = request.data)
        if serial.is_valid():
            self.perform_create(serial)
            return Response({"Status":"success" , "data":serial.data} , status=status.HTTP_201_CREATED)
        
        return Response({"status":"Error" ,"Error":serial.errors } , status=status.HTTP_403_FORBIDDEN)
            
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerial
    name = "MessageViewSet"  
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body"]
    permission_classes = [IsSenderOfMessage]
    pagination_class = LargeResultPagination
    
    
    
    
    def get_queryset(self):
        
        conversation_id = self.kwargs.get("conversation_pk",None)
        
        if conversation_id:
            return Message.objects.filter(conversation_id = conversation_id)
        
          
        return super().get_queryset()
            
    
    
    def create(self, request, *args, **kwargs):
        
        serial = self.get_serializer(data =request.data)
        
        if serial.is_valid():
            self.perform_create(serial)
            
            return Response({
                "status":"Success" , "data":serial.data
            }, status=status.HTTP_201_CREATED) 
            
        return Response({"status": "error" , "Error":serial.errors} , status=status.HTTP_403_FORBIDDEN)