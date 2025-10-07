from django.db import models


class Guest(models.Model):
    user = models.CharField(max_length=100)
    e_mail = models.EmailField()
    text_message = models.TextField()
    data_time_message = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} <{self.e_mail}> @ {self.data_time_message:%Y-%m-%d %H:%M}"


class LabUser(models.Model):
    """Простая модель пользователя для демонстрации хранения паролей.

    ВАЖНО: Это демонстрационная модель для учебных целей. В реальных системах
    следует использовать встроенную модель `django.contrib.auth.User` и её
    механизмы хеширования.
    """

    username = models.CharField(max_length=150, unique=True)
    # Поле хранит либо открытый текст (для демонстрации уязвимости), либо хеш
    password = models.CharField(max_length=255)
    is_hashed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"  # Требование: выводить содержимое таблицы "user"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.username} (hashed={self.is_hashed})"
