from django.urls import path

from users.views import SignUpView, home_display_view, CustomLoginView, display_profile, increase_balance, payment

urlpatterns = [
    path('', home_display_view, name='home'),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', display_profile, name='profile'),
    path('increase/balance/', increase_balance, name='increase_balance'),
    path('payment/', payment, name='payment'),

]
