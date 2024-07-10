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
from gmao.models import Piece
from django.utils import timezone
from gmao.utils import filter_active_doleances

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


# @login_required
# @user_passes_test(lambda u: u.role == 'ADMIN')
# def get_equipe_details(request, equipe_id):
#     equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
#
#     # Récupérer les techniciens de l'équipe
#     personnel_ids = list(equipe.get_personnel_ids())
#     techniciens = Personnel.objects.using('kimei_db').filter(id__in=personnel_ids)
#
#     # Récupérer les doléances associées à l'équipe
#     doleance_ids = list(
#         DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe).values_list('doleance_id', flat=True))
#     doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)
#
#     # Préparer les données des techniciens
#     techniciens_data = [
#         {
#             'id': tech.id,
#             'nom': tech.nom_personnel,
#             'prenom': tech.prenom_personnel,
#             'matricule': tech.matricule,
#             'statut': tech.statut,
#             'poste': tech.poste.nom_poste if tech.poste else None
#         }
#         for tech in techniciens
#     ]
#
#     # Préparer les données des doléances
#     doleances_data = [
#         {
#             'id': dol.id,
#             'ndi': dol.ndi,
#             'statut': dol.statut,
#             'panne_declarer': dol.panne_declarer,
#             'date_transmission': dol.date_transmission.isoformat() if dol.date_transmission else None,
#             'date_deadline': dol.date_deadline.isoformat() if dol.date_deadline else None,
#             'station': {
#                 'id': dol.station.id,
#                 'libelle': dol.station.libelle_station,
#                 'client': dol.station.client.nom_client if dol.station.client else None
#             },
#             'element': dol.element,
#             'commentaire': dol.commentaire
#         }
#         for dol in doleances
#     ]
#
#     # Construire la réponse JSON
#     equipe_details = {
#         'id': equipe.id,
#         'nom': equipe.nom,
#         'description': equipe.description,
#         'techniciens': techniciens_data,
#         'doleances': doleances_data
#     }
#
#     return JsonResponse(equipe_details)


logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_equipe_details(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)

    # Récupérer les techniciens de l'équipe
    personnel_ids = list(equipe.get_personnel_ids())
    techniciens = Personnel.objects.using('kimei_db').filter(id__in=personnel_ids)

    # Récupérer les doléances associées à l'équipe
    doleance_ids = list(
        DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe).values_list('doleance_id', flat=True))

    # Filtrer les doléances
    # today = timezone.now().date()
    doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)
    doleances = filter_active_doleances(doleances)

    # Préparer les données des techniciens
    techniciens_data = [
        {
            'id': tech.id,
            'nom': tech.nom_personnel,
            'prenom': tech.prenom_personnel,
            'matricule': tech.matricule,
            'statut': tech.statut,
            'poste': tech.poste.nom_poste if tech.poste else None
        }
        for tech in techniciens
    ]

    # Préparer les données des doléances
    doleances_data = [
        {
            'id': dol.id,
            'ndi': dol.ndi,
            'statut': dol.statut,
            'panne_declarer': dol.panne_declarer,
            'date_transmission': dol.date_transmission.isoformat() if dol.date_transmission else None,
            'date_deadline': dol.date_deadline.isoformat() if dol.date_deadline else None,
            'station': {
                'id': dol.station.id,
                'libelle': dol.station.libelle_station,
                'client': dol.station.client.nom_client if dol.station.client else None
            },
            'element': dol.element,
            'commentaire': dol.commentaire
        }
        for dol in doleances
    ]

    # Construire la réponse JSON
    equipe_details = {
        'id': equipe.id,
        'nom': equipe.nom,
        'description': equipe.description,
        'techniciens': techniciens_data,
        'doleances': doleances_data
    }

    return JsonResponse(equipe_details)


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
        doleance_equipe, created = DoleanceEquipe.objects.get_or_create(equipe=equipe, doleance_id=doleance_id)

        if created:
            message = 'Doléance attribuée avec succès'
        else:
            message = 'Doléance réintégrée avec succès'

        # Vérifiez si l'attribution existe déjà
        # if DoleanceEquipe.objects.filter(equipe=equipe, doleance_id=doleance_id).exists():
        #     return JsonResponse({'success': False, 'error': 'Cette doléance est déjà attribuée à cette équipe'},
        #                         status=400)

        # Créez l'attribution
        # DoleanceEquipe.objects.create(equipe=equipe, doleance_id=doleance_id)
        return JsonResponse({'success': True, 'message': message})
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
    today = timezone.now().date()
    # Ensuite, sélectionnez les doléances qui ne sont pas dans cette liste
    doleances = (Doleance.objects.using('kimei_db')
                 .filter(
        Q(id__in=doleances_attribuees, statut__in=['ATP', 'ATD'], intervention__top_terminer__date=today) |
        ~Q(id__in=doleances_attribuees)
    )
                 .exclude(statut='TER'))

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


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_pieces_non_attribuees(request):
    search_query = request.GET.get('search', '')

    # Obtenez d'abord tous les IDs des pièces déjà attribuées
    pieces_attribuees = list(PieceDoleanceEquipe.objects.using('teams_db').values_list('piece_id', flat=True))

    # Ensuite, sélectionnez les pièces qui ne sont pas dans cette liste
    pieces = Piece.objects.using('kimei_db').exclude(id__in=pieces_attribuees)

    # Appliquer le filtre de recherche
    if search_query:
        pieces = pieces.filter(
            Q(piece_libelle__icontains=search_query) |
            Q(piece_reference__icontains=search_query)
        )

    # Trier par libellé
    pieces = pieces.order_by('piece_libelle')[:1000]  # Limiter à 1000 résultats pour des raisons de performance

    return JsonResponse({'pieces': list(pieces.values('id', 'piece_libelle', 'piece_reference', 'prix_achat'))})


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
@require_http_methods(["POST"])
def attribuer_piece(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    piece_id = request.POST.get('piece_id')
    doleance_id = request.POST.get('doleance_id')
    quantite = request.POST.get('quantite', 1)

    if not piece_id or not doleance_id:
        return JsonResponse({'success': False, 'error': 'ID de la pièce ou de la doléance manquant'}, status=400)

    doleance_equipe, created = DoleanceEquipe.objects.get_or_create(equipe=equipe, doleance_id=doleance_id)
    piece = get_object_or_404(Piece, id=piece_id)

    PieceDoleanceEquipe.objects.update_or_create(
        doleance_equipe=doleance_equipe,
        piece=piece,
        defaults={'quantite': quantite}
    )

    return JsonResponse({'success': True, 'message': 'Pièce attribuée avec succès'})


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
@require_http_methods(["POST"])
def retirer_piece(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    piece_id = request.POST.get('piece_id')
    doleance_id = request.POST.get('doleance_id')

    if not piece_id or not doleance_id:
        return JsonResponse({'success': False, 'error': 'ID de la pièce ou de la doléance manquant'}, status=400)

    try:
        doleance_equipe = DoleanceEquipe.objects.get(equipe=equipe, doleance_id=doleance_id)
        PieceDoleanceEquipe.objects.filter(doleance_equipe=doleance_equipe, piece_id=piece_id).delete()
        return JsonResponse({'success': True, 'message': 'Pièce retirée avec succès'})
    except (DoleanceEquipe.DoesNotExist, PieceDoleanceEquipe.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Association pièce-doléance non trouvée'}, status=404)
