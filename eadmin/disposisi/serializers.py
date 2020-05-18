from django.contrib.auth.models import User

from rest_framework import serializers

from .models import MemoSimple


class MemoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoSimple
        fields = ['id', 'subject', 'information', 'state', 'sender', ]
        read_only_fields = ['state', ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']