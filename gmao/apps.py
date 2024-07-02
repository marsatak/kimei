from django.apps import AppConfig
from django.db.models.signals import post_save


class GmaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gmao'

    def ready(self):
        from .models import Personnel
        from django.contrib.auth import get_user_model
        from django.contrib.auth.hashers import make_password

        def create_or_update_employee(sender, instance, created, **kwargs):
            Employee = get_user_model()

            employee, created = Employee.objects.using('auth_db').get_or_create(
                matricule=instance.matricule,
                defaults={
                    'username': instance.matricule,
                    'password': make_password('motdepasse123'),
                    'first_name': instance.prenom_personnel,
                    'last_name': instance.nom_personnel,
                    'email': f"{instance.matricule}@example.com",
                    'is_active': instance.is_active,
                    'poste': instance.poste.nom_poste if instance.poste else None,
                    'statut': instance.statut,
                    'num1': instance.num1,
                    'num2': instance.num2,
                    'num3': instance.num3,
                    'adresse': instance.adresse,
                    'last_visite_medical': instance.last_visite_medical,
                    'cin': instance.cin
                }
            )

            if not created:
                employee.first_name = instance.prenom_personnel
                employee.last_name = instance.nom_personnel
                employee.is_active = instance.is_active
                employee.poste = instance.poste.nom_poste if instance.poste else None
                employee.statut = instance.statut
                employee.num1 = instance.num1
                employee.num2 = instance.num2
                employee.num3 = instance.num3
                employee.adresse = instance.adresse
                employee.last_visite_medical = instance.last_visite_medical
                employee.cin = instance.cin
                employee.save(using='auth_db')

        post_save.connect(create_or_update_employee, sender=Personnel, dispatch_uid="update_employee_from_personnel")
