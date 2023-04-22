from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="index"),
    path('get_all_users/', views.get_all_users, name="get_all_users"),
    path('user/', csrf_exempt(views.Users.as_view()), name="user"),

    # 
]