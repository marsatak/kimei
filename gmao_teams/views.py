from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Equipe, EquipePersonnel, DoleanceEquipe
from gmao.models import Personnel, Doleance
from django.db.models import Exists, OuterRef


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def gestion_equipes(request):
    return render(request, 'gmao_teams/gestion_equipes.html')


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def creer_equipe(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        equipe = Equipe.objects.create(nom=nom, description=description)
        return JsonResponse({'success': True, 'id': equipe.id})
    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def liste_equipes(request):
    equipes = Equipe.objects.all()
    return JsonResponse({'equipes': list(equipes.values())})


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_equipe_details(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
    personnel_ids = list(equipe.get_personnel_ids())
    doleance_ids = list(equipe.get_doleance_ids())

    techniciens = Personnel.objects.using('kimei_db').filter(id__in=personnel_ids)
    doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)

    return JsonResponse({
        'nom': equipe.nom,
        'description': equipe.description,
        'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel')),
        'doleances': list(doleances.values('id', 'ndi', 'panne_declarer'))
    })


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def affecter_technicien(request, equipe_id):
    if request.method == 'POST':
        equipe = get_object_or_404(Equipe, id=equipe_id)
        technicien_id = request.POST.get('technicien')
        technicien = get_object_or_404(Personnel, id=technicien_id)
        EquipePersonnel.objects.create(equipe=equipe, personnel=technicien)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def attribuer_doleance(request, equipe_id):
    if request.method == 'POST':
        equipe = get_object_or_404(Equipe, id=equipe_id)
        doleance_id = request.POST.get('doleance')
        doleance = get_object_or_404(Doleance, id=doleance_id)
        DoleanceEquipe.objects.create(equipe=equipe, doleance=doleance)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def retirer_technicien(request, equipe_id):
    if request.method == 'POST':
        equipe = get_object_or_404(Equipe, id=equipe_id)
        technicien_id = request.POST.get('technicien')
        EquipePersonnel.objects.filter(equipe=equipe, personnel_id=technicien_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def retirer_doleance(request, equipe_id):
    if request.method == 'POST':
        equipe = get_object_or_404(Equipe, id=equipe_id)
        doleance_id = request.POST.get('doleance')
        DoleanceEquipe.objects.filter(equipe=equipe, doleance_id=doleance_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_techniciens_disponibles(request):
    # Obtenez d'abord tous les IDs des techniciens déjà affectés
    techniciens_affectes = list(EquipePersonnel.objects.using('teams_db').values_list('personnel_id', flat=True))

    # Ensuite, sélectionnez les techniciens qui ne sont pas dans cette liste
    techniciens = Personnel.objects.using('kimei_db').filter(
        poste__type='TECH',
        statut='PRS'
    ).exclude(id__in=techniciens_affectes)

    return JsonResponse({'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel'))})


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_doleances_non_attribuees(request):
    # Obtenez d'abord tous les IDs des doléances déjà attribuées
    doleances_attribuees = list(DoleanceEquipe.objects.using('teams_db').values_list('doleance_id', flat=True))

    # Ensuite, sélectionnez les doléances qui ne sont pas dans cette liste
    doleances = Doleance.objects.using('kimei_db').filter(statut='NEW').exclude(id__in=doleances_attribuees)

    return JsonResponse({'doleances': list(doleances.values('id', 'ndi', 'panne_declarer'))})
