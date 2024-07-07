from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import DoleanceEquipe, PieceDoleanceEquipe
from gmao.models import Piece


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
@require_http_methods(["POST"])
def affecter_piece(request, equipe_id, doleance_id):
    doleance_equipe = get_object_or_404(DoleanceEquipe, equipe_id=equipe_id, doleance_id=doleance_id)
    piece_id = request.POST.get('piece_id')
    quantite = request.POST.get('quantite', 1)

    if not piece_id:
        return JsonResponse({'success': False, 'error': 'ID de la pièce manquant'}, status=400)

    piece = get_object_or_404(Piece, id=piece_id)

    PieceDoleanceEquipe.objects.update_or_create(
        doleance_equipe=doleance_equipe,
        piece=piece,
        defaults={'quantite': quantite}
    )

    return JsonResponse({'success': True, 'message': 'Pièce affectée avec succès'})


@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def get_equipe_details(request, equipe_id):
    equipe = get_object_or_404(Equipe.objects.using('teams_db'), id=equipe_id)
    personnel_ids = list(equipe.get_personnel_ids())

    doleance_ids = list(
        DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe).values_list('doleance_id', flat=True))

    doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)
    active_doleance_ids = []
    for doleance in doleances:
        if doleance.statut != 'TER':
            active_doleance_ids.append(doleance.id)
        else:
            DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe, doleance_id=doleance.id).delete()

    doleances = Doleance.objects.using('kimei_db').filter(id__in=active_doleance_ids)

    techniciens = Personnel.objects.using('kimei_db').filter(id__in=personnel_ids)

    doleances_data = []
    for doleance in doleances:
        doleance_equipe = DoleanceEquipe.objects.using('teams_db').get(equipe=equipe, doleance_id=doleance.id)
        pieces = PieceDoleanceEquipe.objects.using('teams_db').filter(doleance_equipe=doleance_equipe).select_related(
            'piece')
        pieces_data = [{'id': pe.piece.id, 'libelle': pe.piece.piece_libelle, 'quantite': pe.quantite} for pe in pieces]
        doleances_data.append({
            'id': doleance.id,
            'ndi': doleance.ndi,
            'panne_declarer': doleance.panne_declarer,
            'pieces': pieces_data
        })

    return JsonResponse({
        'nom': equipe.nom,
        'description': equipe.description,
        'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel')),
        'doleances': doleances_data
    })
