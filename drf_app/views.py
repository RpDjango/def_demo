from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
import json
from django.views.generic.base import View

def index(request):
    try:    
        # 1/0
        # raise ModuleNotFoundError('Module not found')
        return JsonResponse({'message': 'This is index api'}, status=200)
    except ModuleNotFoundError as e:
        return JsonResponse({'message': f'Something went wrong- {str(e)}'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Something went wrong- {str(e)}'}, status=500)


def get_all_users(request):
    users = User.objects.all()
    users = serializers.serialize('json',users)
    return JsonResponse(json.loads(users), safe=False)

class Users(View):
    def get(self,request):
        users = User.objects.all()
        users = serializers.serialize('json',users)
        return JsonResponse(json.loads(users), safe=False)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        # user = serializers.serialize('json',user)
        return JsonResponse({'message': 'successfully created'}, safe=False)