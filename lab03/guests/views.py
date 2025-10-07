from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Guest


def list_vulnerable(request):
    # No validation, no escaping: deliberately vulnerable rendering
    if request.method == "POST":
        Guest.objects.create(
            user=request.POST.get("user", ""),
            e_mail=request.POST.get("e_mail", ""),
            text_message=request.POST.get("text_message", ""),
        )
        return redirect("vulnerable")

    entries = Guest.objects.order_by("-data_time_message")
    return render(request, "guests/vulnerable.html", {"entries": entries})


def list_safe(request):
    errors = {}
    # Basic server-side validation and consistently escaped output
    if request.method == "POST":
        user = request.POST.get("user", "").strip()
        email = request.POST.get("e_mail", "").strip()
        text = request.POST.get("text_message", "").strip()

        if not user:
            errors["user"] = "Имя обязательно."
        try:
            validate_email(email)
        except ValidationError:
            errors["e_mail"] = "Неверный формат e-mail."
        if not text:
            errors["text_message"] = "Сообщение обязательно."

        if not errors:
            Guest.objects.create(user=user, e_mail=email, text_message=text)
            return redirect("safe")

    entries = Guest.objects.order_by("-data_time_message")
    return render(request, "guests/safe.html", {"entries": entries, "errors": errors})

# Create your views here.
