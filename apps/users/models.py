from django.contrib.auth.models import User
from django.db import models

class AuthUserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_user_extra')
    code = models.CharField(max_length=50)
    img = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'auth_user_extra'
