from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (CustomLoginView, RegisterView, ResetConfirmView, ResetPasswordView, UserBlock, UserDetailView,
                    UserListView, UserUpdateView, VerifyView)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("verify/<str:token>/", VerifyView.as_view(), name="verify"),
    path("reset/", ResetPasswordView.as_view(), name="reset"),
    path("reset/<str:token>/", ResetConfirmView.as_view(), name="reset_confirm"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("profile/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("profile/<int:pk>/block/", UserBlock.as_view(), name="user_block"),
]
