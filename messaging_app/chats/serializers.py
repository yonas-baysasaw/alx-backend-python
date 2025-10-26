from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password 

class UserSerial (serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs ={"password" :{"write_only":True}}
       
    
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Password does not match")
        
        attrs.pop("confirm_password")
        return super().validate(attrs) 
    
    def create(self , validated_data):
        password = validated_data.get("password")
        validated_data["password"] = make_password(password)
       
        return super().create(validated_data)
    
    
class MessageSerial(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all() , source = "sender_id" , write_only = True)
    
    class Meta:
        model = Message
        fields = ["message_id" , "message_body","sent_at" ,"sender_id"]
    
    def validate_message_body(self , body):
       if len(body.strip())==0:
           raise serializers.ValidationError("Message body can not be empty")
       
       return body  


class ConvsersationSerial(serializers.ModelSerializer):
    participant = serializers.SerializerMethodField()
    participant_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all()  , write_only = True)
    
    
    class Meta:
        model = Conversation
        fields = "__all__"
    def get_participant(self , obj):
        
        return [user.username for user in obj.participants_id.all()]     



