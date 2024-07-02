from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('TECH', 'Technicien'),
    )
    first_login = models.BooleanField(default=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='TECH')
    matricule = models.CharField(max_length=10, unique=True)
    poste = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=3, choices=[
        ('PRS', 'Présent'),
        ('ABS', 'Absent'),
        ('ATT', 'Tâche Attribuée'),
        ('INT', 'En intervention'),
    ], default='ABS')
    num1 = models.CharField(max_length=13, blank=True, null=True)
    num2 = models.CharField(max_length=13, blank=True, null=True)
    num3 = models.CharField(max_length=13, blank=True, null=True)
    adresse = models.CharField(max_length=50, blank=True, null=True)
    last_visite_medical = models.DateTimeField(blank=True, null=True)
    cin = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        db_table = 'accounts_employee'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matricule})"
