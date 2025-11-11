from django.contrib import admin

from .models import CustomerAccount


@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "status", "balance", "updated_at")
    search_fields = ("full_name", "email")
    list_filter = ("status",)
