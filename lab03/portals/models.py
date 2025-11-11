from django.db import models


class CustomerAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        BLOCKED = "blocked", "Заблокирован"
        PENDING = "pending", "Ожидает подтверждения"

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("full_name",)
        verbose_name = "учетная запись клиента"
        verbose_name_plural = "учетные записи клиентов"

    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"
