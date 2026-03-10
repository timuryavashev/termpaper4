import secrets
from django.core.mail import send_mail

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.contrib import messages

from config.settings import SITE_URL, EMAIL_HOST_USER
from users.forms import CustomUserCreationForm
from users.models import CustomUser



class RegisterView(CreateView):
    model = CustomUser
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()

        user.generate_token()

        messages.success(self.request, 'Проверьте email для подтверждения')
        return super().form_valid(form)


class VerifyView(View):
    def get(self, request, token):
        user = get_object_or_404(CustomUser, token=token)
        user.is_verified = True
        user.token = ''
        user.save()
        messages.success(request, 'Email подтвержден')
        return redirect('users:login')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()

        if user.is_blocked:
            messages.error(self.request, 'Пользователь заблокирован')
            return self.form_invalid(form)

        if not user.is_verified:
            messages.error(self.request, 'Email не подтвержден')
            return self.form_invalid(form)


        return super().form_valid(form)


class ResetPasswordView(View):

    def post(self, request):
        email = request.POST.get('email')
        try:
            user =  get_object_or_404(CustomUser, email=email)
            token = secrets.token_urlsafe(30)
            user.token = token
            user.save()
            send_mail('Сброс пароля',
                     f'{SITE_URL}/reset/{token}/',
                     EMAIL_HOST_USER, [email])
            messages.success(request, 'Проверьте email')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email не найден')
        return redirect('users:login')

    def get(self, request):
        return render(request, 'users/reset_password.html')


class ResetConfirmView(View):
    def get(self, request, token):
        user = get_object_or_404(CustomUser, token=token)
        return render(request, 'users/reset_confirm.html', {'token': token})

    def post(self, request, token):
        user = get_object_or_404(CustomUser, token=token)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'users/reset_confirm.html', {'token': token})

        user.set_password(password1)
        user.token = ''
        user.save()
        messages.success(request, 'Пароль изменен')
        return redirect('users:login')
