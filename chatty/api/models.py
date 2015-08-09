from django.db import models


class ChatroomUser(models.Model):

    name = models.CharField(max_length=20, unique=True)


class Chatroom(models.Model):

    name = models.CharField(max_length=20)
    members = models.ManyToManyField(ChatroomUser)

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()

    def join(self, user):
        self.members.add(user)

    def leave(self, user):
        if user in self.members.all():
            self.members.remove(user)

class ChatroomMessage(models.Model):

    room = models.ForeignKey(Chatroom, related_name='messages')
    user = models.ForeignKey(ChatroomUser, related_name='messages')
    body = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)