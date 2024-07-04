from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from .models import Equipe, EquipePersonnel, DoleanceEquipe
from gmao.models import Personnel, Doleance


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def creer_equipe(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        equipe = Equipe.objects.create(nom=nom, description=description)
        return JsonResponse({'success': True, 'id': equipe.id})
    return render(request, 'gmao_teams_old/templates/gmao_teams/creer_equipe.html')


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def liste_equipes(request):
    equipes = Equipe.objects.all()
    return render(request, 'gmao_teams_old/templates/gmao_teams/liste_equipes.html', {'equipes': equipes})


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def affecter_technicien(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)

    if request.method == 'POST':
        technicien_id = request.POST.get('technicien')
        technicien = get_object_or_404(Personnel.objects.using('kimei_db'), id=technicien_id)
        EquipePersonnel.objects.using('teams_db').create(equipe=equipe, personnel_id=technicien.id)
        return JsonResponse({'success': True})
    techniciens_affectes_ids = set(EquipePersonnel.objects.using('teams_db').values_list('personnel_id', flat=True))
    # Pour les requêtes GET
    techniciens = Personnel.objects.using('kimei_db').all().filter(
        statut='PRS',
        poste__type='Terrain'
    ).exclude(id__in=techniciens_affectes_ids)
    print(f"Nombre total de personnels : {techniciens.count()}")

    return render(request, 'gmao_teams_old/templates/gmao_teams/affecter_technicien.html',
                  {'equipe': equipe, 'techniciens': techniciens})


# def affecter_technicien(request, equipe_id):
#     equipe = get_object_or_404(Equipe, id=equipe_id)
#     if request.method == 'POST':
#         technicien_id = request.POST.get('technicien')
#         technicien = get_object_or_404(Personnel, id=technicien_id)
#         EquipePersonnel.objects.using('teams_db').create(equipe=equipe, personnel=technicien)
#         return JsonResponse({'success': True})
#     techniciens = Personnel.objects.filter(poste__type='TECH')
#     return render(request, 'gmao_teams/affecter_technicien.html', {'equipe': equipe, 'techniciens': techniciens})

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def attribuer_doleance(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)

    if request.method == 'POST':
        doleance_id = request.POST.get('doleance')
        doleance = get_object_or_404(Doleance.objects.using('kimei_db'), id=doleance_id)
        DoleanceEquipe.objects.using('teams_db').create(equipe=equipe, doleance_id=doleance.id)
        return JsonResponse({'success': True})

    doleances = Doleance.objects.using('kimei_db').filter(statut='NEW')
    return render(request, 'gmao_teams_old/templates/gmao_teams/attribuer_doleance.html',
                  {'equipe': equipe, 'doleances': doleances})


@login_required
def get_techniciens_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
    personnel_ids = equipe.get_personnel_ids()
    techniciens = Personnel.objects.using('kimei_db').filter(id__in=personnel_ids)
    return JsonResponse({'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel'))})


@login_required
def get_doleances_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
    doleance_ids = equipe.get_doleance_ids()
    doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)
    return JsonResponse({'doleances': list(doleances.values('id', 'ndi', 'panne_declarer'))})


def retirer_technicien(request, equipe_id, technicien_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
    EquipePersonnel.objects.using('teams_db').filter(equipe=equipe, personnel_id=technicien_id).delete()
    return redirect('nom_de_votre_vue_detail_equipe', equipe_id=equipe_id)


def portefeuille_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)

    doleance_ids = DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe).values_list('doleance_id', flat=True)

    doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids, statut='NEW')

    return render(request, 'gmao_teams_old/templates/gmao_teams/portefeuille_equipe.html', {
        'equipe': equipe,
        'doleances': doleances
    })


def prendre_en_charge_doleance(request, equipe_id, doleance_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
    doleance = get_object_or_404(Doleance.objects.using('kimei_db'), id=doleance_id)

    if doleance.statut == 'NEW':
        doleance.statut = 'INT'  # En intervention
        doleance.date_debut = timezone.now()
        doleance.save(using='kimei_db')

    return redirect('portefeuille_equipe', equipe_id=equipe.id)
