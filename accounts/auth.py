from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from gmao.models import Personnel


class PersonnelAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(matricule=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            try:
                personnel = Personnel.objects.using('kimei_db').get(matricule=username)
                user = UserModel.objects.create(
                    username=username,
                    matricule=username,
                    first_name=personnel.prenom_personnel,
                    last_name=personnel.nom_personnel,
                    email=f"{username}@example.com",
                    is_active=personnel.is_active,
                    statut=personnel.statut,
                    num1=personnel.num1,
                    num2=personnel.num2,
                    num3=personnel.num3,
                    adresse=personnel.adresse,
                    last_visite_medical=personnel.last_visite_medical,
                    cin=personnel.cin,
                    poste=personnel.poste.nom_poste if personnel.poste else None
                )
                user.set_password(password)
                user.save()
                if user.check_password(password):
                    return user
            except Personnel.DoesNotExist:
                return None

        return None
