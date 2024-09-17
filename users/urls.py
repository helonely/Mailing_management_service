from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, PasswordResetView, profile_edit, profile_detail

app_name = UsersConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('edit-profile/', profile_edit, name='profile_edit'),
    path('detail/', profile_detail, name='profile_detail'),
]
