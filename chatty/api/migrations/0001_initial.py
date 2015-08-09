# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chatroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ChatroomMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=160)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(related_name='messages', to='api.Chatroom')),
            ],
        ),
        migrations.CreateModel(
            name='ChatroomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='chatroommessage',
            name='user',
            field=models.ForeignKey(related_name='messages', to='api.ChatroomUser'),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='members',
            field=models.ManyToManyField(to='api.ChatroomUser'),
        ),
    ]
