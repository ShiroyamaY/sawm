from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from users.models import User

from .forms import CustomerAccountForm
from .models import CustomerAccount


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles: tuple[str, ...] = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.allowed_roles and request.user.role not in self.allowed_roles:
            raise PermissionDenied("Доступ к этой зоне запрещен для вашей роли.")
        return super().dispatch(request, *args, **kwargs)


class AdminPanelView(RoleRequiredMixin, TemplateView):
    template_name = "portals/admin_panel.html"
    allowed_roles = (User.Role.ADMIN,)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["users"] = User.objects.order_by("username")
        ctx["recent_accounts"] = CustomerAccount.objects.order_by("-updated_at")[:5]
        return ctx


class ManagerWorkspaceView(RoleRequiredMixin, TemplateView):
    template_name = "portals/manager/dashboard.html"
    allowed_roles = (User.Role.MANAGER,)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        accounts = CustomerAccount.objects.all()
        ctx["accounts_total"] = accounts.count()
        ctx["pending_count"] = accounts.filter(status=CustomerAccount.Status.PENDING).count()
        ctx["blocked_count"] = accounts.filter(status=CustomerAccount.Status.BLOCKED).count()
        ctx["recent_accounts"] = accounts.order_by("-updated_at")[:3]
        return ctx


class AccountListView(RoleRequiredMixin, ListView):
    model = CustomerAccount
    template_name = "portals/manager/accounts_list.html"
    context_object_name = "accounts"
    allowed_roles = (User.Role.MANAGER,)


class AccountCreateView(RoleRequiredMixin, CreateView):
    form_class = CustomerAccountForm
    template_name = "portals/manager/account_form.html"
    success_url = reverse_lazy("manager-accounts")
    allowed_roles = (User.Role.MANAGER,)

    def form_valid(self, form):
        messages.success(self.request, "Учётная запись успешно создана.")
        return super().form_valid(form)


class AccountUpdateView(RoleRequiredMixin, UpdateView):
    model = CustomerAccount
    form_class = CustomerAccountForm
    template_name = "portals/manager/account_form.html"
    success_url = reverse_lazy("manager-accounts")
    allowed_roles = (User.Role.MANAGER,)

    def form_valid(self, form):
        messages.success(self.request, "Данные клиента обновлены.")
        return super().form_valid(form)


class AccountDeleteView(RoleRequiredMixin, DeleteView):
    model = CustomerAccount
    template_name = "portals/manager/account_confirm_delete.html"
    success_url = reverse_lazy("manager-accounts")
    allowed_roles = (User.Role.MANAGER,)

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, "Учётная запись удалена.")
        return super().delete(request, *args, **kwargs)
