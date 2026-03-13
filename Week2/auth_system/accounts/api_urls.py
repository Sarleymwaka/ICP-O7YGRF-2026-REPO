from django.urls import path
from . import views 

urlpatterns = [
    ##paths for endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('reset-password/', views.PasswordResetRequestView.as_view(), name='reset-password'),
    path('reset-confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='reset-confirm'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh')
]