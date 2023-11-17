from django.db import models
from django.contrib.auth.models import User

class BloodType(models.Model):
    type = models.CharField(max_length=3)

    def __str__(self):
        return self.type
    class Meta:
        db_table = "blood_type"
class Gender(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "Gender"


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to="patients",blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    class Meta:
        db_table = "patients"
