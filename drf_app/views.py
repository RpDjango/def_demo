from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core import serializers
import json
from rest_framework.permissions import IsAuthenticated
from django.views.generic.base import View
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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
        user = serializers.serialize('json',[user,])
        return JsonResponse({'message': json.loads(user)}, safe=False)

@csrf_exempt   
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'message': 'User doesnt exist'})

        if user:
            is_user = authenticate(request, username=username, password=password)
            if is_user:
                login(request, user)
                request.session['user'] = user
                
                result = {}
                tokens = get_tokens_for_user(user)
                result['access'] = tokens['access']
                result['refresh'] = tokens['refresh']
                return result
                # return redirect('/')
            else:
                return JsonResponse({'message': 'password is incorrect'})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
class Employees(viewsets.ViewSet):
    query_set = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Employee.objects.all()
        users = EmployeeSerializer(users, many=True)
        return Response(users.data, status=200)
    
    @permission_classes(IsAuthenticated)
    def post(self, request):
        data = request.body
        data = json.loads(data)
        emp_obj = Employee.objects.create(**data)
        serializer = EmployeeSerializer(emp_obj)
        return Response(serializer.data, status=201)