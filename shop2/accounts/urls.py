from django.urls import path
from .views import user_login, user_logout, UserRegisterVertifyCode, user_register, UserInfoView, ForgotPasswordView, ForgotPasswordVertifyView, ForgotPasswordNewView

app_name = "accounts"

urlpatterns = [

    path("user_login/", user_login, name="user_login"),
    path("user_register/", user_register, name="user_register"),
    path("user_logout/", user_logout, name="user_logout"),
    path("user_register_vertify/", UserRegisterVertifyCode.as_view(), name="register_vertify"),
    path("user_info/", UserInfoView.as_view(), name="user_info"),
    path("forgot_password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("forgot_password/vertify/", ForgotPasswordVertifyView.as_view(), name="forgot_password_vertify"),
    path("forgot_password/new_password/", ForgotPasswordNewView.as_view(), name="new_password"),

]