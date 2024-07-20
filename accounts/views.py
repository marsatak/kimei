from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.db import migrations
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
import logging

from gmao.models import Personnel  # Assurez-vous d'importer le modèle Personnel
from .models import Employee
from django.utils import timezone
from django.db import transaction
from gmao.models import Pointage
from django.utils import timezone
from accounts.models import Employee
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# DÉBOGGAGE
logger = logging.getLogger(__name__)


# ###################### DÉBUT TRAITEMEMENT CHANGEMENT DE MOT DE PASSE #############################
def change_password(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    User = get_user_model()
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            user.set_password(new_password)
            user.first_login = False
            user.save()
            update_session_auth_hash(request, user)

            # Authentifiez l'utilisateur explicitement
            authenticated_user = authenticate(request, username=user.username, password=new_password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Votre mot de passe a été changé avec succès.')
                return redirect('gmao:home')
            else:
                messages.error(request, 'Erreur lors de la connexion après le changement de mot de passe.')
        else:
            messages.error(request, 'Les mots de passe ne correspondent pas.')

    return render(request, 'accounts/change_password.html', context)


# ###################### FIN TRAITEMEMENT CHANGEMENT DE MOT DE PASSE #############################


# ###################### DÉBUT TRAITEMEMENT DE L'AUTHENTIFICATION #############################


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                # Utiliser 'kimei_db' pour Personnel
                personnel = Personnel.objects.using('kimei_db').get(matricule=user.matricule)

                # Vérifier si c'est la première connexion de la journée
                today = timezone.now().date()
                employee = Employee.objects.using('auth_db').get(id=user.id)
                first_login_of_day = employee.last_login is None or employee.last_login.date() < today

                if first_login_of_day:
                    # Mettre à jour le statut du personnel seulement s'il n'est pas en INT ou ATT
                    if personnel.statut not in ['INT', 'ATT']:
                        personnel.statut = 'PRS'
                        personnel.save(using='kimei_db')

                    # Mettre à jour le statut de l'employé seulement s'il n'est pas en INT ou ATT
                    if employee.statut not in ['INT', 'ATT']:
                        employee.statut = 'PRS'
                        employee.save(using='auth_db')

                # Mettre à jour last_login
                employee.last_login = timezone.now()
                employee.save(using='auth_db')

                # Connexion de l'utilisateur
                login(request, user)
                request.session['last_activity'] = timezone.now().isoformat()

                if user.first_login:
                    return redirect('accounts:change_password')

                return redirect('gmao:home')

            except ObjectDoesNotExist:
                return render(request, 'registration/login.html', {'error': 'Utilisateur ou personnel non trouvé'})

        else:
            return render(request, 'registration/login.html', {'error': 'Identifiants invalides'})

    return render(request, 'registration/login.html')


# @csrf_exempt
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             request.session['last_activity'] = timezone.now().isoformat()
#             # Mise à jour du statut de l'utilisateur
#             user.statut = 'PRS'
#             user.save()
#
#             # Mise à jour du statut du personnel correspondant
#             try:
#                 personnel = Personnel.objects.get(matricule=user.matricule)
#                 personnel.statut = 'PRS'
#                 personnel.save()
#             except Personnel.DoesNotExist:
#                 # Log this error or handle it as appropriate for your application
#                 pass
#
#             if user.first_login:
#                 return redirect('accounts:change_password')
#
#             return redirect('gmao:home')
#         else:
#             return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'registration/login.html')


# ###################### FIN TRAITEMEMENT DE L'AUTHENTIFICATION #############################

# ###################### TRAITEMEMENT AUTHENT AVEC SESSION KEY MONOLOGIN #############################
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             # Vérifiez si l'utilisateur a une session_key existante
#             # if user.session_key:
#             # Si oui, vérifiez si cette session existe toujours
#             # from django.contrib.sessions.models import Session
#             # try:
#             #     Session.objects.get(session_key=user.session_key)
#             #     messages.error(request, "Vous êtes déjà connecté sur un autre appareil.")
#             #     return render(request, 'registration/login.html',
#             #                   {'error': 'Already logged in elsewhere'})
#             # except Session.DoesNotExist:
#             #     # Si la session n'existe plus, réinitialisez la session_key
#             #     user.session_key = None
#
#             login(request, user)
#             # Mise à jour de la session_key après la connexion
#             user.session_key = request.session.session_key
#             user.statut = 'PRS'
#             user.save()
#
#             if user.first_login:
#                 return redirect('accounts:change_password')
#
#             return redirect('gmao:home')
#         else:
#             return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'registration/login.html')
# ###################### FIN TRAITEMEMENT AUTHENT AVEC SESSION KEY MONOLOGIN #############################

# ###################### DÉBUT TRAITEMEMENT FIN DE SESSION #############################
def logout_view(request):
    User = get_user_model()
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        # user.session_key = None
        user.statut = 'ABS'
        user.save()
    # Assurez-vous que la session est complètement effacée
    request.session.flush()
    return redirect('gmao:home')


# ###################### FIN TRAITEMEMENT FIN DE SESSION #############################


# ###################### MIGRATION PERSONNELS VERS EMPOYEES #############################
@user_passes_test(lambda u: u.is_superuser)
def run_employee_migration(request):
    from .migrations.xxxx_create_employees_from_personnel import create_employees_from_personnel
    create_employees_from_personnel(apps, migrations.recorder.MigrationRecorder)
    return HttpResponse("Migration completed")
# ###################### FIN MIGRATION PERSONNELS VERS EMPOYEES #############################
