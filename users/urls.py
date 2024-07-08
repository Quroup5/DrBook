from django.contrib.auth.views import LoginView
from django.urls import path, include

from users.forms import LoginForm
from users.views import SignUpView, home_display_view

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(form_class=LoginForm,
                                     template_name='users/login.html'), name='login'),
    path('', home_display_view, name='home')

]
