
from django.conf import settings
from django.core.mail import send_mail


def send_new_password(email, new_password):

    send_mail(
        'Вы обновили пароль!',
        f'Ваша новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )