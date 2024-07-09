from django.contrib.auth.views import LoginView
from django.urls import path, include

from users.forms import LoginForm
from users.views import SignUpView, home_display_view, CustomLoginView, display_profile

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', home_display_view, name='home'),
    path('profile/', display_profile, name='profile')
]
