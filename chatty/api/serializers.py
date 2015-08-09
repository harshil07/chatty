from rest_framework import serializers
from .models import Chatroom, ChatroomUser, ChatroomMessage


class ChatroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatroom
        fields = ['id', 'name']


class ChatroomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatroomUser
        fields = ['id', 'name']

class ChatroomMessageSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.name')

    class Meta:
        model = ChatroomMessage
        fields = ['body', 'user']