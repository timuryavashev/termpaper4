from django.urls import path
from .views import RegisterView, CustomLoginView, VerifyView, ResetPasswordView, ResetConfirmView
from django.contrib.auth.views import LogoutView


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing:home'), name='logout'),
    path('verify/<str:token>/', VerifyView.as_view(), name='verify'),
    path('reset/', ResetPasswordView.as_view(), name='reset'),
    path('reset/<str:token>/', ResetConfirmView.as_view(), name='reset_confirm'),
]