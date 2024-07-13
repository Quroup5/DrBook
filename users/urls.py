from django.urls import path
from users.views import UserRegisterView, UserLoginView, home, otp

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('home/', home, name='home'),
    path('otp/', otp, name='otp'),
]

# urlpatterns = [
#     path('', home_display_view, name='home'),
#     path('signup/', SignUpView.as_view(), name="signup"),
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('profile/', display_profile, name='profile'),
#     path('increase/balance/', increase_balance, name='increase_balance'),
#     path('payment/', payment, name='payment'),
#
# ]
