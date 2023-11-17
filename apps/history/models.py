from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        # Añade más acciones aquí si es necesario
    ]

    SECTION_CHOICES = [
        ('section1', 'Section 1'),
        ('section2', 'Section 2'),
        # Añade más secciones aquí si es necesario
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField()
    section_type = models.CharField(max_length=20, choices=SECTION_CHOICES)
    
    class Meta:
        db_table = "history"
