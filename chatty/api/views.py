import datetime
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import viewsets
from .serializers import (
    ChatroomSerializer, ChatroomMessageSerializer, 
    ChatroomUserSerializer
)
from .models import Chatroom, ChatroomMessage, ChatroomUser


class ChatroomUserViewSet(viewsets.ModelViewSet):

    queryset = ChatroomUser.objects.all()
    serializer_class = ChatroomUserSerializer

    @detail_route(methods=['get'])
    def get_messages(self, request, pk):
        chatroom_user = self.get_object()
        last_message_time = request.GET.get('last_message_time')
        member_chatrooms = Chatroom.objects.filter(members=chatroom_user)
        chatroom_messages = ChatroomMessage.objects.filter(
            room__in=member_chatrooms)
        if last_message_time:
            chatroom_messages = chatroom_messages.filter(
                created_at__gt=last_message_time)
        else:
            chatroom_messages = chatroom_messages.none()
        data = ChatroomMessageSerializer(chatroom_messages, many=True).data
        return Response(data)


class ChatroomViewSet(viewsets.ModelViewSet):

    queryset = Chatroom.objects.all()
    serializer_class = ChatroomSerializer

    @detail_route(methods=['post'])
    def join(self, request, pk):
        chatroom = self.get_object()
        user = request.data.get('user')
        if not user:
            return Response({'error': 'Missing parameter user'}, 
                status=status.HTTP_400_BAD_REQUEST)
        try:
            chatroom_user = ChatroomUser.objects.get(name=user)
        except ChatroomUser.DoesNotExist:
            return Response({'error': 'Bad user provided'}, 
                status=status.HTTP_400_BAD_REQUEST)

        chatroom.join(chatroom_user)
        return Response({'success': True})

    @detail_route(methods=['post'])
    def leave(self, request, pk):
        chatroom = self.get_object()
        user = request.data.get('user')
        if not user:
            return Response({'error': 'Missing parameter user'}, 
                status=status.HTTP_400_BAD_REQUEST)

        chatroom_user = ChatroomUser.objects.get(name=user)
        chatroom.leave(chatroom_user)
        return Response({'success': True})

    @detail_route(methods=['get'])
    def members(self, request, pk):
        chatroom = self.get_object()
        members = chatroom.members.all()
        data = ChatroomUserSerializer(members, many=True).data
        return Response(data)

    @detail_route(methods=['post'])
    def send_message(self, request, pk):
        chatroom = self.get_object()
        message = request.data.get('message')
        user = request.data.get('user')
        chatroom_user = ChatroomUser.objects.get(name=user)

        if not chatroom.is_member(chatroom_user):
            return Response({'errors': 'You are not a member of the chatroom'}, 
                status=status.HTTP_401_UNAUTHORIZED) 

        chatroom_message = ChatroomMessage.objects.create(
            user=chatroom_user, body=message, room=chatroom)
        data = ChatroomMessageSerializer(chatroom_message).data
        return Response(data)

    @detail_route(methods=['get'])
    def get_messages(self, request, pk):
        chatroom = self.get_object()
        last_message_time = request.GET.get('last_message_time')
        chatroom_messages = ChatroomMessage.objects.filter(room=chatroom)
        if last_message_time:
            chatroom_messages = chatroom_messages.filter(
                created_at__gt=last_message_time)
        else:
            chatroom_messages = chatroom_messages.none()

        data = ChatroomMessageSerializer(chatroom_messages, many=True).data
        return Response(data)