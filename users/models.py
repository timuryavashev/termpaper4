from django.db import models
import secrets
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from config.settings import EMAIL_HOST_USER, SITE_URL


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    country = models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)
    token = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    def generate_token(self):
        self.token = secrets.token_urlsafe(30)
        self.save()
        send_mail('Подтвердите email',
                  f'{SITE_URL}/verify/{self.token}/',
                  EMAIL_HOST_USER, [self.email])
