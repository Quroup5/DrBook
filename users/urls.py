from django.urls import path

from users.views import SignUpView, CustomLoginView, display_profile, increase_balance, payment, otp, \
    UserLoginView, home

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', display_profile, name='profile'),
    path('increase/balance/', increase_balance, name='increase_balance'),
    path('payment/', payment, name='payment'),
    path('otp/', otp, name='otp'),
    path('home/', home, name='home'),

]
