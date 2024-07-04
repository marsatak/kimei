from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.db import migrations

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from gmao.models import Personnel  # Assurez-vous d'importer le modèle Personnel
from .models import Employee
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#             if user.first_login:
#                 # Rediriger vers la page de changement de mot de passe
#                 request.session['user_id'] = user.id
#                 return redirect('accounts:change_password')
#             login(request, user)
#
#             # Mettre à jour le statut du personnel
#             try:
#                 print('Updating personnel status', user)
#                 personnel = Personnel.objects.get(matricule=username)
#                 personnel.statut = 'PRS'
#                 personnel.save()
#             except Personnel.DoesNotExist:
#                 messages.warning(request, "Profil personnel non trouvé.")
#
#             return redirect('gmao:home')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'accounts/login.html')
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 personnel = Personnel.objects.get(matricule=username)
#                 if personnel.statut not in ['ATT', 'INT']:
#                     personnel.statut = 'PRS'
#                     personnel.save()
#             except Personnel.DoesNotExist:
#                 messages.warning(request, "Profil personnel non trouvé.")
#             return redirect('gmao:home')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'accounts/login.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 personnel = Personnel.objects.get(matricule=username)
#                 if personnel.statut not in ['ATT', 'INT']:
#                     personnel.statut = 'PRS'
#                     personnel.save()
#             except Personnel.DoesNotExist:
#                 messages.warning(request, "Profil personnel non trouvé.")
#             return redirect('gmao:home')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'accounts/login.html')


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.session_key and user.session_key != request.session.session_key:
                messages.error(request, "Vous êtes déjà connecté sur un autre appareil.")
                return render(request, 'accounts/login.html', {'error': 'Already logged in elsewhere'})

            login(request, user)
            user.session_key = request.session.session_key
            user.statut = 'PRS'
            user.save()

            if user.first_login:
                return redirect('accounts:change_password')

            return redirect('gmao:home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')


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


# def logout_view(request):
#     user = request.user
#     user.statut = 'ABS'
#     user.save()
#     logout(request)
#     return redirect('login')


# Create your views here.
# MIRE BIENVENUE


def logout_view(request):
    if request.user.is_authenticated:
        user = request.user
        user.session_key = None
        user.statut = 'ABS'
        user.save()
    logout(request)
    return redirect('login')


def index(request):
    return render(request, 'accounts/index.html')


@user_passes_test(lambda u: u.is_superuser)
def run_employee_migration(request):
    from .migrations.xxxx_create_employees_from_personnel import create_employees_from_personnel
    create_employees_from_personnel(apps, migrations.recorder.MigrationRecorder)
    return HttpResponse("Migration completed")
