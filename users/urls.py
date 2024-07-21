from django.urls import path

from .views import SignUpView, display_profile, increase_balance, payment, otp, see_doctor_comments, save_comment, add_comment, UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('profile/', display_profile, name='profile'),
    path('increase/balance/', increase_balance, name='increase_balance'),
    path('payment/', payment, name='payment'),
    path('visit/time/addcomment', add_comment, name='add_comment'),
    path('visit/time/savecomment', save_comment, name='save_comment'),
    path('comments/display', see_doctor_comments, name='see_doctor_comments'),

    path('otp/', otp, name='otp'),
]
