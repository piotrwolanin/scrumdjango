from django.urls import path
from accounts.views import UserLogIn, UserLogOut, UserPasswordChange
from django.views.generic.base import RedirectView


app_name = 'accounts'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='accounts:login')),
    path('login/', UserLogIn.as_view(), name='login'),
    path('logout/', UserLogOut.as_view(), name='logout'),
    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
]
