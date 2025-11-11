from django.contrib import admin
from .models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("user", "e_mail", "data_time_message")
    search_fields = ("user", "e_mail", "text_message")
