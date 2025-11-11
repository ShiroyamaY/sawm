from django import forms

from .models import CustomerAccount


class CustomerAccountForm(forms.ModelForm):
    class Meta:
        model = CustomerAccount
        fields = ("full_name", "email", "status", "balance", "notes")
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
