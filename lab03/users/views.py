from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import User


class RoleLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        user_role = getattr(self.request.user, "role", User.Role.MANAGER)
        if user_role == User.Role.ADMIN:
            return reverse_lazy("admin-panel")
        if user_role == User.Role.MANAGER:
            return reverse_lazy("manager-workspace")
        return super().get_success_url()


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, "Вы вышли из системы. Для продолжения пройдите аутентификацию.")
    return redirect("login")
