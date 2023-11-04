from django.urls import path
from .views import register, logOut, home, user_login, activate

urlpatterns = [
    path('', home, name='home'),
    path('index/', home, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logOut/', logOut, name='logOut'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
