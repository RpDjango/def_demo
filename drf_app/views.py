from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    try:    
        raise ValueError("Test error")
        # return JsonResponse({'message': 'This is index api'})
    except Exception as e:
        return JsonResponse({'message': f'Something went wrong- {str(e)}'})
