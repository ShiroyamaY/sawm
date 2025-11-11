from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import Guest


def list_vulnerable(request):
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
    errors: dict[str, str] = {}
    if request.method == "POST":
        user = request.POST.get("user", "").strip()
        email = request.POST.get("e_mail", "").strip()
        text = request.POST.get("text_message", "").strip()

        if not user:
            errors["user"] = "??? ??????????? ??? ??????????."
        try:
            validate_email(email)
        except ValidationError:
            errors["e_mail"] = "??????? ?????????? ????? ??????????? ?????."
        if not text:
            errors["text_message"] = "????????? ?? ????? ???? ??????."

        if not errors:
            Guest.objects.create(user=user, e_mail=email, text_message=text)
            return redirect("safe")

    entries = Guest.objects.order_by("-data_time_message")
    return render(request, "guests/safe.html", {"entries": entries, "errors": errors})
