import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER, SITE_URL
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()

        user.generate_token()

        messages.success(self.request, "Проверьте email для подтверждения")
        return super().form_valid(form)


class VerifyView(View):
    def get(self, request, token):
        user = get_object_or_404(CustomUser, token=token)
        user.is_verified = True
        user.token = ""
        user.save()
        messages.success(request, "Email подтвержден")
        return redirect("users:login")


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        user = form.get_user()

        if user.is_blocked:
            messages.error(self.request, "Пользователь заблокирован")
            return self.form_invalid(form)

        if not user.is_verified:
            messages.error(self.request, "Email не подтвержден")
            return self.form_invalid(form)

        return super().form_valid(form)


class ResetPasswordView(View):

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = get_object_or_404(CustomUser, email=email)
            token = secrets.token_urlsafe(30)
            user.token = token
            user.save()
            send_mail("Сброс пароля", f"{SITE_URL}/reset/{token}/", EMAIL_HOST_USER, [email])
            messages.success(request, "Проверьте email")
        except CustomUser.DoesNotExist:
            messages.error(request, "Email не найден")
        return redirect("users:login")

    def get(self, request):
        return render(request, "users/reset_password.html")


class ResetConfirmView(View):
    def get(self, request, token):
        user = get_object_or_404(CustomUser, token=token)
        return render(request, "users/reset_confirm.html", {"token": token})

    def post(self, request, token):
        user = get_object_or_404(CustomUser, token=token)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Пароли не совпадают")
            return render(request, "users/reset_confirm.html", {"token": token})

        user.set_password(password1)
        user.token = ""
        user.save()
        messages.success(request, "Пароль изменен")
        return redirect("users:login")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"
    context_object_name = "custom_user"

    def dispatch(self, request, *args, **kwargs):
        custom_user = self.get_object()
        if request.user != custom_user and not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет права для просмотра информации")
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    fields = [
        "avatar",
        "first_name",
        "last_name",
        "country",
        "phone_number",
    ]

    def dispatch(self, request, *args, **kwargs):
        custom_user = self.get_object()

        print(f"DEBUG: Current user: {request.user.email}, ID: {request.user.id}")
        print(f"DEBUG: Target user: {custom_user.email}, ID: {custom_user.id}")
        print(f"DEBUG: Has perm can_block_user: {request.user.has_perm('users.can_block_user')}")

        if request.user != custom_user:
            return HttpResponseForbidden("У вас нет права для изменения информации")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.object.pk])


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    context_object_name = "custom_users"
    permission_required = "users.can_block_user"


class UserBlock(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "users.can_block_user"

    def post(self, request, pk):
        custom_user = get_object_or_404(CustomUser, pk=pk)
        if custom_user.is_blocked:
            custom_user.is_blocked = False
        else:
            custom_user.is_blocked = True
        custom_user.save()
        return redirect("users:user_detail", pk=pk)
