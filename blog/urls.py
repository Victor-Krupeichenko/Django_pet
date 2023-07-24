from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("register-user/", RegisterUser.as_view(), name="register_user"),
    path("login-user/", LoginUser.as_view(), name="login_user"),
    path("update-user/<int:pk>/", UpdateUser.as_view(), name="update_user"),
    path("logout-user/", user_logout, name="logout_user"),
    path("delete-user/<int:pk>/", DeleteUser.as_view(), name="delete_user"),
]
