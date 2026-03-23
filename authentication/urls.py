from django.urls import path

from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('users/', views.RegistrationAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view()),
]