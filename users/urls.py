from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
]
