from exchange import serializers
from exchange.lib import request_client
from django.shortcuts import render
from django.contrib.auth import get_user_model

from exchange.models import LevelFee
from .models import (
    ChatSession, ChatSessionMessage, deserialize_user
)
from exchange.serializers import AdminChatSerializer, LevelFeeSerializer
from rest_framework import status
from rest_framework import authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

class ChatSessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        if not request.data['email']:
            user = request.user
        else: 
            email= request.data['email']
        if not request.data['email']:
            chats =  ChatSession.objects.filter(owner = request.user)
        else:
            chats =  ChatSession.objects.filter(email = email)
        for item in chats :
            item.delete()
        if not request.data['email']:
            chat_session = ChatSession.objects.create(owner=user)
        else:
            chat_session = ChatSession.objects.create(email=email)
        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': 'New chat session created'
        })


class ChatSessionMessageView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']

        chat_session = ChatSession.objects.get(uri=uri)
        messages = [chat_session_message.to_json() 
            for chat_session_message in chat_session.messages.all()]
        notseen = 0
        for item in chat_session.messages.all():
            if not item.seen:
                notseen = notseen + 1
        return Response({
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages, 'notseen' : notseen
        })

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']
        if not request.data['email']:
            user = request.user
        else: 
            email= request.data['email']
        chat_session = ChatSession.objects.get(uri=uri)
        if request.data['email']:
            ChatSessionMessage.objects.create(
                email=email, chat_session=chat_session, message=message, seen=True
            )
        if request.user.is_staff:
            ChatSessionMessage.objects.create(
                user=user, chat_session=chat_session, message=message, aseen=True
            )
        else:
            ChatSessionMessage.objects.create(
                user=user, chat_session=chat_session, message=message, seen=True
            )
        return Response ({
            'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message,
            'user': deserialize_user(user)
        })

class user(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        if len(ChatSession.objects.filter(email = request.data['email'])) > 0 :
            user = ChatSession.objects.get(email = request.data['email'])
            return Response({'uri' : user.uri , 'username' : user.email})
        if len(ChatSession.objects.filter(owner = request.user)) > 0 :
            user = ChatSession.objects.get(owner = request.user)
            return Response({'uri' : user.uri , 'username' : request.user.username})
        return Response({'uri' : 0})

class seen(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]
    def get(self, request, uri, *args, **kwargs):
        if request.user.is_staff:
            chat_session = ChatSession.objects.get(uri=uri)
            messages = chat_session.messages.all()
            for item in messages:
                item.aseen = True
                item.save()
            return Response(True)
        chat_session = ChatSession.objects.get(uri=uri)
        messages = chat_session.messages.all()
        for item in messages:
            item.seen = True
            item.save()
        return Response(True)

class adminchat(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        user = ChatSession.objects.all()
        serializer = AdminChatSerializer(user , many=True)
        return Response(serializer.data)


