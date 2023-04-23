from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="index"),
    path('get_all_users/', views.get_all_users, name="get_all_users"),
    path('user/', csrf_exempt(views.Users.as_view()), name="user"),
    path('user_login/', views.user_login, name='user_login'),
    path('employee/', views.Employees.as_view({'get':'get', 'post': 'post'}), name='employee'),

    # 
]