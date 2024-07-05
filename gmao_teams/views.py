from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Equipe, EquipePersonnel, DoleanceEquipe
from gmao.models import Personnel, Doleance
from accounts.models import Employee
from django.db.models import Exists, OuterRef
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q

import logging


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


# @login_required
# @user_passes_test(lambda u: u.role == 'ADMIN')
# def get_equipe_details(request, equipe_id):
#     equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
#     personnel_ids = list(equipe.get_personnel_ids())
#     doleance_ids = list(equipe.get_doleance_ids())
#
#     techniciens = Personnel.objects.using('kimei_db').filter(id__in=personnel_ids)
#     doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)
#
#     return JsonResponse({
#         'nom': equipe.nom,
#         'description': equipe.description,
#         'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel')),
#         'doleances': list(doleances.values('id', 'ndi', 'panne_declarer'))
#     })
@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_equipe_details(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
    personnel_ids = list(equipe.get_personnel_ids())

    # Récupérer toutes les doléances associées à l'équipe
    doleance_ids = list(
        DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe).values_list('doleance_id', flat=True))

    # Vérifier le statut de chaque doléance
    doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)
    active_doleance_ids = []
    for doleance in doleances:
        if doleance.statut != 'TER':  # Si la doléance n'est pas terminée
            active_doleance_ids.append(doleance.id)
        else:
            # Supprimer l'association pour les doléances terminées
            DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe, doleance_id=doleance.id).delete()

    # Mettre à jour la liste des doléances actives
    doleances = Doleance.objects.using('kimei_db').filter(id__in=active_doleance_ids)

    techniciens = Personnel.objects.using('kimei_db').filter(id__in=personnel_ids)

    return JsonResponse({
        'nom': equipe.nom,
        'description': equipe.description,
        'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel')),
        'doleances': list(doleances.values('id', 'ndi', 'panne_declarer'))
    })


logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
@require_http_methods(["POST"])
@ensure_csrf_cookie
def affecter_technicien(request, equipe_id):
    logger.info(f"Tentative d'affectation de technicien pour l'équipe {equipe_id}")
    logger.info(f"Méthode de requête: {request.method}")
    logger.info(f"Données POST: {request.POST}")

    try:
        equipe = get_object_or_404(Equipe, id=equipe_id)
        technicien_id = request.POST.get('technicien')

        if not technicien_id:
            logger.error("ID du technicien manquant")
            return JsonResponse({'success': False, 'error': 'ID du technicien manquant'}, status=400)

        logger.info(f"ID du technicien: {technicien_id}")
        technicien = get_object_or_404(Personnel, id=technicien_id)

        # Vérifiez si l'affectation existe déjà
        if EquipePersonnel.objects.filter(equipe=equipe, personnel_id=technicien.id).exists():
            logger.warning(f"Le technicien {technicien_id} est déjà affecté à l'équipe {equipe_id}")
            return JsonResponse({'success': False, 'error': 'Ce technicien est déjà affecté à cette équipe'},
                                status=400)

        EquipePersonnel.objects.create(equipe=equipe, personnel_id=technicien.id)
        logger.info(f"Technicien {technicien_id} affecté avec succès à l'équipe {equipe_id}")
        return JsonResponse({'success': True})

    except Exception as e:
        logger.exception(f"Erreur lors de l'affectation du technicien: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def attribuer_doleance(request, equipe_id):
    if request.method == 'POST':
        equipe = get_object_or_404(Equipe, id=equipe_id)
        doleance_id = request.POST.get('doleance')

        # Vérifiez si la doléance existe
        doleance = get_object_or_404(Doleance, id=doleance_id)

        # Vérifiez si l'attribution existe déjà
        if DoleanceEquipe.objects.filter(equipe=equipe, doleance_id=doleance_id).exists():
            return JsonResponse({'success': False, 'error': 'Cette doléance est déjà attribuée à cette équipe'},
                                status=400)

        # Créez l'attribution
        DoleanceEquipe.objects.create(equipe=equipe, doleance_id=doleance_id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)


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
    techniciens = (Personnel.objects.using('kimei_db').filter(
        poste_id__in=(1, 2, 4, 6, 7, 12, 13, 17, 18),
        statut='PRS'
    )
                   .exclude(id__in=techniciens_affectes))

    return JsonResponse({'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel'))})


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_doleances_non_attribuees(request):
    search_query = request.GET.get('search', '')

    # Obtenez d'abord tous les IDs des doléances déjà attribuées
    doleances_attribuees = list(DoleanceEquipe.objects.using('teams_db').values_list('doleance_id', flat=True))

    # Ensuite, sélectionnez les doléances qui ne sont pas dans cette liste
    doleances = (Doleance.objects.using('kimei_db')
                 .exclude(statut='TER')
                 .exclude(id__in=doleances_attribuees))

    # Appliquer le filtre de recherche
    if search_query:
        doleances = doleances.filter(
            Q(ndi__icontains=search_query) |
            Q(panne_declarer__icontains=search_query) |
            Q(station__libelle_station__icontains=search_query)
        )

    # Trier par date de transmission décroissante
    doleances = doleances.order_by('-date_transmission')[
                :1000]  # Limiter à 1000 résultats pour des raisons de performance

    return JsonResponse({'doleances': list(
        doleances.values('id', 'ndi', 'panne_declarer', 'date_transmission', 'station__libelle_station'))})
