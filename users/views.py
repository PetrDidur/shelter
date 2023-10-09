from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView

from dogs.templates.dogs.services import send_new_password
from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('dogs:index')
    
    """def form_valid(self, form):
        new_user = form.save()
        send_mail(
             subject='Поздравляем с регистрацией!',
             message='Вы зарегистрировались!',
             from_email=settings.EMAIL_HOST_USER,
             recipient_list=[new_user.email],
             fail_silently=False
         )
        return super().form_valid(form)"""


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):  # возвращает текущего пользователя
        return self.request.user


@login_required
def generate_new_password(request):
    password = get_random_string(10)
    email = request.user.email
    request.user.set_password(password)
    request.user.save()
    send_new_password(email, password)

    return redirect(reverse('users:login'))


        
    

