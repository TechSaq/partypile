from django.db import models
from django.contrib.auth.models import User


class AuthUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.user.username  # type: ignore

    class Meta:
        verbose_name_plural = "AuthUsers"
