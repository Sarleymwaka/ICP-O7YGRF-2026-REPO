from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    #paths for frontend
    path('', views.index, name='index'),
    path('reset.html/', views.reset_page, name='reset_page'),
    path('register.html/', views.register_page, name='register.html'),
    path('login.html/', views.login_page, name='login.html'),

]