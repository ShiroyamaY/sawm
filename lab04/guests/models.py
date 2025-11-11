from django.db import models


class Guest(models.Model):
    user = models.CharField(max_length=100)
    e_mail = models.EmailField()
    text_message = models.TextField()
    data_time_message = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} <{self.e_mail}> @ {self.data_time_message:%Y-%m-%d %H:%M}"


class LabUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    is_hashed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.username} (hashed={self.is_hashed})"
