from django.contrib import admin
from .models import Guest, LabUser


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("user", "e_mail", "data_time_message")
    search_fields = ("user", "e_mail", "text_message")


@admin.register(LabUser)
class LabUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_hashed", "created_at")
    search_fields = ("username",)
