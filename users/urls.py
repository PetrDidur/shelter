from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, UserRegisterForm, generate_new_password

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password')
]