from rest_framework_nested import routers
from .views import *
from django.urls import include ,path

app_name = "chats"

router = routers.DefaultRouter()

router.register("conversations" , ConversationViewSet , basename=ConversationViewSet.name)

message_conversation_router = routers.NestedDefaultRouter(router,r'conversations' , lookup = "conversation")

message_conversation_router.register(r"messages" , MessageViewSet , basename="conversation-messages")



urlpatterns = [
    path("" , include(router.urls)),
    path("" , include(message_conversation_router.urls))
    
]
