from django.db.models import Q
from gmao.models import Piece


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
