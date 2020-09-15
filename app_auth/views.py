from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from pytz import unicode
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
import json
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from knox.auth import TokenAuthentication


CLIENT_ID = '839455990561-ipb3cdo4982dnmbds6gk6pj7c2r81bsk.apps.googleusercontent.com'


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    return HttpResponse("Django world")


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)


@csrf_exempt
def register_user(request):
    return HttpResponse(request.body)


def register_user(request):
    context = {}
    return render(request, 'app_auth/index.html', context)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def knox_validation(request):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)

@csrf_exempt
def validate_token(request):
    if request.method == 'POST':
        data = request.POST
        id_token = data['idtoken']
        info = dvalidate_token(id_token)
        if info != None:
            try:
                user = User.objects.get(username=info['sub'])
                # return HttpResponse("User present")
            except Exception:
                user = register_new_user(info)
                # return HttpResponse("User not exit created new one")
            finally:
                return JsonResponse({
                    "username": user.username,
                    "token": AuthToken.objects.create(user)[1]
                })
        return HttpResponse("Invalid Token")
    return HttpResponse('Not a POST request')


def register_new_user(info):
    user = User.objects.create_user(info['sub'], info['email'])
    user.save()
    return user

def dvalidate_token(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        data = {
            "sub": idinfo['sub'],
            "email": idinfo['email']
        }
        return data
    except ValueError:
        # Invalid token
        return None